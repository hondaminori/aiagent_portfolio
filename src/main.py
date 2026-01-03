from dotenv import load_dotenv
from common.paths import ENV_PATH
from preprocessing.source import load_documents
from preprocessing.normalize import normalize_documents
from preprocessing.chunk import chunk_documents
from preprocessing.embed import create_embedding
from query.service import create_service_from_env
import os

load_dotenv(ENV_PATH)

# 環境変数の取得
api_key = os.getenv("OPENAI_API_KEY")
embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
chat_model_name = os.getenv("CHAT_MODEL_NAME")

documents = load_documents()

normalized_documents = normalize_documents(documents)

chunked_documents = chunk_documents(normalized_documents)

embeddings = create_embedding(api_key, embedding_model_name)

# vectordb = build_vectorstore(
#     documents=chunked_documents,
#     embedding=embeddings,
#     collection_name="WorkRules"
# )

# vectordb = load_vectorstore(
#     embedding=embeddings,
#     collection_name="WorkRules"
# )

service = create_service_from_env(
    api_key=api_key,
    embedding_model_name=embedding_model_name,
    chat_model_name=chat_model_name,
    collection_name="WorkRules",
    k=3,
    search_type="similarity",
    )

print(service.ask("退職金について教えてください。"))
