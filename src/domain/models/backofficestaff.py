# メンションするユーザーの情報を保持するクラス
class BackofficeStaff:
    def __init__(self, user_name: str, slack_id: str):
        self.user_name = user_name
        self.slack_id = slack_id
        self.is_mention = False
