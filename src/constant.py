MODEL = "gpt-4o"
EMBEDDING = "text-embedding-3-small"
PROMPT = "hwchase17/openai-functions-agent"
AWS_REGION = "ap-northeast-1"
AWS_S3_BUCKET = "aibot-data"
RETRIEVER_NAME = "qa_source_data"
RETRIEVER_DESCRIPTION = (
    "バックオフィスのQ&Aの情報が含まれている。このデータを使うことで適切に回答できる。"
)
VECTORSTORE_NAME = "backoffice-vectorstore"
VECTORSTORE_DESCRIPTION = "バックオフィスのデータをベクトル化したデータベース"
DATA_DIRECTORY = "data"
VECTORSTORE_PATH = "vectorstore"
BACKOFFICE_STAFF_PATH = "backoffice_staff"
