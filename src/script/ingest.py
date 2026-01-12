from common.bootstrap import init_app
from rag_core.preprocessing.source import load_documents
from rag_core.preprocessing.normalize import normalize_documents
from rag_core.preprocessing.chunk import chunk_documents
from rag_core.preprocessing.embed import create_embedding
from rag_core.preprocessing.vector_backend import build_vectorstore
import logging

init_app("ingest")

logger = logging.getLogger(__name__)

def main() -> None:
    docs = load_documents()
    normalized_docs = normalize_documents(docs)
    chunked_docs = chunk_documents(normalized_docs)

    embedding = create_embedding()

    build_vectorstore(
        embedding=embedding,
        documents=chunked_docs
    )

    logger.info(f"{__file__}が成功しました。")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception(f"Ingest に失敗しました。")
        raise
