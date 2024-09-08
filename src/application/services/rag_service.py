import re

import constant as constant
from application.interfaces.rag_agent import RagAgent


class RAGService:
    def __init__(
        self,
        rag_agent: RagAgent,
    ):
        self.rag_agent = rag_agent

    def chat(self, message: str) -> str:
        answer = self.rag_agent.get(message)

        return convert_markdown_to_mrkdwn(answer)


# markdown形式からmrkdwn（slack用のリッチテキスト）形式に変換
def convert_markdown_to_mrkdwn(text: str) -> str:
    # Markdownの太字(**text**)をSlackのmrkdwn形式(*text*)に変換
    text = re.sub(r"\*\*(.*?)\*\*", r" *\1* ", text)

    # Markdownのリンク([text](url))をSlackのmrkdwn形式(<url|text>)に変換
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"<\2|\1>", text)

    # 通常のリストの変換（- または * で始まる行）
    text = re.sub(r"^(\s*)[-*]\s+", r"\1• ", text, flags=re.MULTILINE)

    return text
