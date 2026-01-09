"""
chunk.py

normalize 済み Document をチャンク分割する。
- 入力: List[Document]
- 出力: List[Document]
"""
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from common.config import CHUNK_SIZE, CHUNK_OVERLAP, TEXT_SPLITTER_SEPARATORS
from common.logging_config import logging
from common.logging_config import log_start_end

logger = logging.getLogger(__name__)

@log_start_end
def chunk_documents(documents: list[Document]) -> list[Document]:
    """
    normalize 済み Document をチャンク分割する。
    変数chunked_docsは不要だが、デバッグ時のために残している。

    Args:
        List[Document]: チャンク分割対象のDocumentリスト
    Returns:
        List[Document]: チャンク分割されたDocumentリスト
    """
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=TEXT_SPLITTER_SEPARATORS
    )

    chunked_docs = recursive_splitter.split_documents(documents)

    for chunked_doc in chunked_docs:
        logger.debug(chunked_doc)

    return chunked_docs
