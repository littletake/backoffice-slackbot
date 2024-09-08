from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from application.services.backoffice_staff import BackofficeStaffService
from application.services.rag_service import RAGService


class SlackBot:
    def __init__(
        self,
        slack_bot_token: str,
        slack_app_token: str,
        rag_service: RAGService,
        backoffice_staff_service: BackofficeStaffService,
    ):
        self.app = App(token=slack_bot_token)
        self.slack_app_token = slack_app_token
        self.rag_service = rag_service
        self.backoffice_staff_service = backoffice_staff_service

        self._setup_handlers()

    def _setup_handlers(self):
        @self.app.event("app_mention")
        def hanndle_memtion(event, say):
            thread_ts = event["ts"]
            say(text="🔄処理中🔄", thread_ts=thread_ts)

            question = event["text"]
            answer = self.rag_service.chat(question)
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": answer,
                    },
                },
            ]

            # botの回答にスタッフが含まれているか確認する
            is_mentioned, _ = self.backoffice_staff_service.check_mentioned_staff(
                answer
            )
            if is_mentioned:
                blocks.append(
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "☝️担当者に連絡する",
                                    "emoji": True,
                                },
                                "action_id": "direct_request",
                            }
                        ],
                    }
                )

            say(text=answer, blocks=blocks, thread_ts=thread_ts)

        @self.app.action("direct_request")
        def hanndle_button(ack, body, say):
            # ボタンのリクエストを確認
            ack()

            # ボット側の返答
            latest_bot_message = body["message"]["text"]

            _, call_message = self.backoffice_staff_service.check_mentioned_staff(
                latest_bot_message
            )

            thread_history = self._fetch_thread_history(
                body["container"]["channel_id"], body["container"]["thread_ts"]
            )
            first_question = thread_history["messages"][0]["blocks"][0]["elements"][0][
                "elements"
            ][1]["text"]
            bot_message = f"{call_message}\n 私ではちょっと厳しそうです... お助けください🙏 \n\n *最初の質問文:* {first_question}"

            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": bot_message,
                    },
                },
            ]
            thread_ts = body["container"]["thread_ts"]

            # 取得したvalueをもとにメッセージを送信
            say(text=bot_message, blocks=blocks, thread_ts=thread_ts)

    # slackのチャンネルの履歴を取得する
    def _fetch_thread_history(self, channel_id: str, thread_ts_id: str):
        conversations_history = self.app.client.conversations_replies(
            channel=channel_id, ts=thread_ts_id
        )
        return conversations_history

    def start(self):
        handler = SocketModeHandler(self.app, self.slack_app_token)
        handler.start()
