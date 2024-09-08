from typing import Any, Dict, List, Optional

from botocore.exceptions import ClientError
from langchain.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS, VectorStore

import constant
from infrastructure.clients.s3 import S3Client


class VectorStoreTool:
    def __init__(
        self,
        s3_client: S3Client,
        openai_embeddings: OpenAIEmbeddings,
        vectorstore_path: str,
        data_directory_path: str,
    ):
        self.s3_client = s3_client
        self.openai_embeddings = openai_embeddings
        self.vectorstore_path = vectorstore_path
        self.data_directory_path = data_directory_path  # vectorstore_pathの一個上階層
        self.tool = None
        self.vectorstore: Optional[VectorStore] = None

    def initialize(self):
        """vectorstoreをlangchain_toolに変換する"""
        # TODO: 差分があればダウンロードするようにする
        self._download_from_s3()
        self.tool = self._load_to_langchain_tool()

    def _download_from_s3(self):
        try:
            self.s3_client.download_folder(
                constant.VECTORSTORE_PATH, self.data_directory_path
            )
        except ClientError as e:
            print(f"Error downloading file from S3: {e}")
            raise

    def _load_to_langchain_tool(self):
        """vectorstoreをロードして、langchainのtoolに変換する

        Returns:
            _type_: _description_
        """
        self.vectorstore = FAISS.load_local(
            self.vectorstore_path, self.openai_embeddings
        )
        if not self.vectorstore:
            raise ValueError("VectorStore not loaded.")
        return [
            create_retriever_tool(
                self.vectorstore.as_retriever(),
                constant.RETRIEVER_NAME,
                constant.RETRIEVER_DESCRIPTION,
            )
        ]

        return

    def _run(self, query: str) -> List[Dict[str, Any]]:
        if not self.vectorstore:
            raise ValueError("VectorStore not initialized. Call initialize() first.")
        results = self.vectorstore.similarity_search(query, k=5)
        return [
            {"content": doc.page_content, "metadata": doc.metadata} for doc in results
        ]

    async def _arun(self, query: str) -> List[Dict[str, Any]]:
        # 非同期バージョンの実装
        return self._run(query)

    def get_tool(self) -> Tool:
        return Tool(
            name=constant.VECTORSTORE_NAME,
            description=constant.VECTORSTORE_DESCRIPTION,
            func=self._run,
        )
