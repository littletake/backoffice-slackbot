import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from server.secret import Secret

import constant as constant


# rawファイルからベクトル化されたデータを作成する
def create_vectorstore(rawdata_path: str, secrets: Secret):
    vectorstore_path = os.path.join(rawdata_path, "vectorstore")
    if not os.path.exists(vectorstore_path):
        loader = DirectoryLoader(rawdata_path, glob="**/*.md")
        documents = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        ).split_documents(loader.load())
        embedding = OpenAIEmbeddings(
            api_key=secrets.openai_api,  # type: ignore
            model=constant.EMBEDDING,
        )
        vector = FAISS.from_documents(documents, embedding)
        vector.save_local(vectorstore_path)


if __name__ == "__main__":
    rawdata_path = os.path.join(os.getcwd(), "raw")
    envfile_path = os.path.join(os.getcwd(), "server", ".env")
    load_dotenv(envfile_path)
    region_name = os.environ.get("APP_ENV")
    secret = Secret(region_name if region_name else "remote")

    create_vectorstore(rawdata_path, secret)
    print("created vectorstore successfully")
