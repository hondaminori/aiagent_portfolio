"""
vector_backend.py

VectorDB の backend を隠蔽するファサード。
Chroma / PostgreSQL などの実装差をここで吸収する。
"""
from langchain_chroma import Chroma
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
        # persist_directory=str(CHROMA_PERSIST_DIR)
        persist_directory='/tmp/chroma'
    )

    return vectordb

def load_vectorstore(
    embedding: OpenAIEmbeddings,
    collection_name: str
):
    """
    永続化された VectorStore（LangChain）のインスタンスを読み込む。

    Args:
        embedding: LangChain の Embeddings 互換オブジェクト（現在は OpenAIEmbeddings）
        collection_name (str): コレクション名
    Returns:
        VectorStore（LangChain）のインスタンス
    """

    vectordb = Chroma(
        collection_name=collection_name,
        embedding_function=embedding,
        persist_directory='/tmp/chroma'
    )

    return vectordb