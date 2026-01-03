"""
vector_backend.py

VectorDB の backend を隠蔽するファサード。
Chroma / PostgreSQL などの実装差をここで吸収する。
"""
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from common.paths import CHROMA_PERSIST_DIR
from typing import List 

def build_vectorstore(
    documents: List[Document],
    embedding: OpenAIEmbeddings,
    collection_name: str
):
    """
    VectorStore（LangChain）のインスタンスを生成する。

    Args:
        documents (List[Document]): ドキュメントリスト
        embedding: LangChain の Embeddings 互換オブジェクト（現在は OpenAIEmbeddings）
        collection_name (str): コレクション名

    Returns:
        VectorStore（LangChain）のインスタンス
    """

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        collection_name=collection_name,
        persist_directory=str(CHROMA_PERSIST_DIR)
    )

    return vectordb
