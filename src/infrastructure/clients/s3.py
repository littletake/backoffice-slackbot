import os

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

import constant


class S3Client:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str):
        self.s3_client = boto3.client(
            "s3",
            region_name=constant.AWS_REGION,
        )

    def upload_file(self, file_name: str, bucket: str, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        if object_name is None:
            object_name = file_name

        try:
            self.s3_client.upload_file(file_name, bucket, object_name)
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
        except ClientError as e:
            print(f"ClientError: {e}")
            return False
        return True

    def download_file(self, bucket: str, object_name: str, file_name: str):
        """S3 bucketからファイルをダウンロードする

        :param bucket: Bucket to download from
        :param object_name: S3 object name to download
        :param file_name: File to save as
        :return: True if file was downloaded, else False
        """
        try:
            self.s3_client.download_file(bucket, object_name, file_name)
        except NoCredentialsError:
            print("Credentials not available")
            return False
        except ClientError as e:
            print(f"ClientError: {e}")
            return False
        return True

    def download_folder(self, folder_name: str, local_dir: str):
        """S3 bucketからフォルダーをダウンロードする"""
        s3_client = boto3.client("s3")
        try:
            paginator = s3_client.get_paginator("list_objects_v2")
            pages = paginator.paginate(
                Bucket=constant.AWS_S3_BUCKET, Prefix=folder_name
            )

            for page in pages:
                if "Contents" in page:
                    for obj in page["Contents"]:
                        file_key = obj["Key"]
                        file_path = os.path.join(local_dir, file_key)

                        if not os.path.exists(os.path.dirname(file_path)):
                            os.makedirs(os.path.dirname(file_path))

                        s3_client.download_file(
                            constant.AWS_S3_BUCKET, file_key, file_path
                        )
                        print(f"Downloaded {file_key} to {file_path}")
        except NoCredentialsError:
            print("Credentials not available")
        except PartialCredentialsError:
            print("Incomplete credentials provided")
        except ClientError as e:
            print(f"An error occurred: {e.response['Error']['Message']}")
        except TypeError as e:
            print(f"Type error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# # s3を使った例
# def _use_s3():
#     s3_handler = S3Client(
#         os.environ.get(constant.AWS_ACCESS_KEY_ID),
#         os.environ.get(constant.AWS_SECRET_ACCESS_KEY),
#         os.environ.get(constant.AWS_REGION),
#     )

#     # ファイルをアップロード
#     file_name_to_upload = "sample.txt"
#     s3_handler.upload_file(file_name_to_upload, constant.AWS_S3_BUCKET)
#     print("Uploaded")

#     # ファイルをダウンロード
#     object_name_to_download = "sample.txt"
#     file_name_to_save = "test.txt"
#     s3_handler.download_file(
#         constant.AWS_S3_BUCKET,
#         object_name_to_download,
#         file_name_to_save,
#     )
#     print("Downloaded")
