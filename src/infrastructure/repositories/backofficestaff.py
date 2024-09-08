# バックオフィスのスタッフ情報を取得するリポジトリ

import os
from typing import List

import pandas as pd
from botocore.exceptions import ClientError

import constant
from domain.models.backofficestaff import BackofficeStaff
from infrastructure.clients.s3 import S3Client

filename = "data.csv"


class BackofficeStaffRepository:
    def __init__(
        self,
        s3_client: S3Client,
        backoffice_staff_file_path: str,
        data_directory_path: str,
    ):
        self.s3_client = s3_client
        self.staffs: List[BackofficeStaff] = []
        self.backoffice_staff_file_path = backoffice_staff_file_path
        self.data_directory_path = data_directory_path  # vectorstore_pathの一個上階層

    def initialize(self):
        # s3からcsvをダウンロードしてきて構造体のリストを作成
        self._download_from_s3()
        self._register_staffs()

    def _download_from_s3(self):
        try:
            self.s3_client.download_file(
                constant.AWS_S3_BUCKET,
                os.path.join(constant.BACKOFFICE_STAFF_PATH, filename),
                self.backoffice_staff_file_path,
            )
        except ClientError as e:
            print(f"Error downloading file from S3: {e}")
            raise

    def _register_staffs(self):
        # CSVファイルを読み込む
        data = pd.read_csv(self.backoffice_staff_file_path)

        # データを基にBackofficeStaff構造体のリストを作成
        self.staffs = [
            BackofficeStaff(row["user_name"], row["slack_id"])
            for _, row in data.iterrows()
        ]

    def register_mentioned_staffs(self, target_text: str):
        """メンションされたスタッフを登録する関数
        対象の文章から社員を検索し、メンションされたかを判定

        Args:
            target_text (str): _description_
        """
        for staff in self.staffs:
            is_mention = staff.user_name in target_text
            staff.is_mention = is_mention

    def create_call_message(self) -> str:
        """メンションされたスタップを呼び出す文を作成する

        Returns:
            str: _description_
        """
        mention_list = []
        for staff in self.staffs:
            if staff.is_mention:
                mention_list.append(f"<@{staff.slack_id}>")
        if len(mention_list) == 0:
            return ""
        return " ".join(mention_list)
