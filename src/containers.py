import os

from dependency_injector import containers, providers
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import constant
from application.services.backoffice_staff import BackofficeStaffService
from application.services.rag_service import RAGService
from infrastructure.agents.rag_agent import RAGAgent
from infrastructure.clients.s3 import S3Client
from infrastructure.repositories.backofficestaff import BackofficeStaffRepository
from infrastructure.tools.vectorstore_tool import VectorStoreTool
from presentation.slack.rag_bot import SlackBot


class Container(containers.DeclarativeContainer):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
    slack_app_token = os.getenv("SLACK_APP_TOKEN")

    config = providers.Configuration()

    data_directory_path = os.path.join(os.getcwd(), constant.DATA_DIRECTORY)
    if not os.path.exists(data_directory_path):
        os.makedirs(data_directory_path)

    vectorstore_path = os.path.join(data_directory_path, constant.VECTORSTORE_PATH)
    if not os.path.exists(vectorstore_path):
        os.makedirs(vectorstore_path)

    backoffice_staff_path = os.path.join(
        data_directory_path, constant.BACKOFFICE_STAFF_PATH
    )
    if not os.path.exists(backoffice_staff_path):
        os.makedirs(backoffice_staff_path)
    backoffice_staff_file_path = os.path.join(
        data_directory_path, constant.BACKOFFICE_STAFF_PATH, "data.csv"
    )

    openai_embeddings = providers.Singleton(
        OpenAIEmbeddings, api_key=openai_api_key, model=constant.EMBEDDING
    )
    llm_client = providers.Singleton(
        ChatOpenAI, api_key=openai_api_key, model=constant.MODEL, temperature=0
    )

    """infrastructure layer providers
    """
    # AssumeRoleを使ってアクセスする場合はkey不要
    s3_client = providers.Singleton(
        S3Client,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
    )
    vectorstore_tool = providers.Singleton(
        VectorStoreTool,
        s3_client=s3_client,
        openai_embeddings=openai_embeddings,
        vectorstore_path=vectorstore_path,
        data_directory_path=data_directory_path,
    )
    backoffice_staff_repository = providers.Singleton(
        BackofficeStaffRepository,
        s3_client=s3_client,
        backoffice_staff_file_path=backoffice_staff_file_path,
        data_directory_path=data_directory_path,
    )
    rag_agent = providers.Singleton(
        RAGAgent,
        llm_client=llm_client,
        vector_store_tool=vectorstore_tool,
    )

    """application layer providers
    """
    rag_service = providers.Singleton(
        RAGService,
        rag_agent=rag_agent,
    )
    backoffice_staff_service = providers.Singleton(
        BackofficeStaffService,
        backoffice_staff_repository=backoffice_staff_repository,
    )

    """presentation layer providers
    """
    slack_bot = providers.Singleton(
        SlackBot,
        slack_bot_token=slack_bot_token,
        slack_app_token=slack_app_token,
        rag_service=rag_service,
        backoffice_staff_service=backoffice_staff_service,
    )
