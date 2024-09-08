from typing import Tuple

from application.interfaces.backoffice_staff import BackofficeStaffRepository


class BackofficeStaffService:
    def __init__(
        self,
        backoffice_staff_repository: BackofficeStaffRepository,
    ):
        self.backoffice_staff_repository = backoffice_staff_repository

    def check_mentioned_staff(self, message: str) -> Tuple[bool, str]:
        # メンションされたスタッフを登録する
        self.backoffice_staff_repository.register_mentioned_staffs(message)

        call_message = self.backoffice_staff_repository.create_call_message()
        if call_message == "":
            return False, ""
        return True, call_message
