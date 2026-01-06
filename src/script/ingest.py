from dotenv import load_dotenv
from common.paths import ENV_PATH
from rag_core.preprocessing.source import load_documents
from rag_core.preprocessing.normalize import normalize_documents
from rag_core.preprocessing.chunk import chunk_documents
from rag_core.preprocessing.embed import create_embedding
from rag_core.preprocessing.vector_backend import build_vectorstore
from common.logging_config import setup_logging
import os

load_dotenv(ENV_PATH, override=True)
setup_logging()

import logging
logger = logging.getLogger(__name__)

def main() -> None:

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

    logger.info(f"Ingest が成功しました。")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception(f"Ingest に失敗しました。")
        raise
