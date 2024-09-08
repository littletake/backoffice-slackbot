from abc import ABC, abstractmethod


class BackofficeStaffRepository(ABC):
    @abstractmethod
    def register_mentioned_staffs(self, target_text: str):
        """メンションされたスタッフを登録する関数
        対象の文章から社員を検索し、メンションされたかを判定

        Args:
            target_text (str): _description_
        """
        pass

    @abstractmethod
    def create_call_message(self) -> str:
        """メンションされたスタップを呼び出す文を作成する

        Returns:
            str: _description_
        """
        pass
