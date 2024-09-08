from abc import ABC, abstractmethod


class RagAgent(ABC):
    @abstractmethod
    def get(self, query: str) -> str:
        """質問に対して回答を返す

        Args:
            query (str): 質問文

        Returns:
            str: 回答文
        """
        pass
