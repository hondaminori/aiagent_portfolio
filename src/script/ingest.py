from dotenv import load_dotenv
from common.paths import ENV_PATH
from preprocessing.source import load_documents
from preprocessing.normalize import normalize_documents
from preprocessing.chunk import chunk_documents
from preprocessing.embed import create_embedding
from preprocessing.vector_backend import build_vectorstore
import os

load_dotenv(ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")
embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")

docs = load_documents()
normalized_docs = normalize_documents(docs)
chunk_docs = chunk_documents(normalized_docs)

embedding = create_embedding(api_key, embedding_model_name)

build_vectorstore(
    embedding=embedding,
    documents=chunk_docs,
    collection_name="WorkRules",
)

print("Ingest completed.")