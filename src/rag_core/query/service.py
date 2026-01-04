"""
service.py

UI（CLI / FastAPI / Streamlit）から呼び出す窓口。
- 起動時に依存物（embedding / vectordb / retriever / chain）を組み立てて保持する
- 問い合わせは ask(query) だけに統一する
"""

from dataclasses import dataclass
from typing import Any

from langchain_openai import ChatOpenAI

from common.prompts import SYSTEM_PROMPT
from rag_core.preprocessing.embed import create_embedding
from rag_core.preprocessing.vector_backend import load_vectorstore
from rag_core.query.retrieve import create_retriever
from rag_core.query.generate import create_chain


@dataclass
class RAGService:
    """RAG 問い合わせ用サービス（UI非依存）"""
    chain: Any

    def ask(self, query: str) -> str:
        """質問を受け取り回答を返す（UIからはこれだけ呼ぶ）"""
        return self.chain.invoke(query)


def create_service_from_env(
    api_key: str,
    embedding_model_name: str,
    chat_model_name: str,
    collection_name: str = "WorkRules",
    k: int = 3,
    search_type: str = "similarity",
) -> RAGService:
    """
    環境変数等で得た設定値から RAGService を組み立てる。
    FastAPI/Streamlitでは「起動時に1回」呼ぶ想定。
    """
    embedding = create_embedding(api_key, embedding_model_name)

    vectordb = load_vectorstore(
        embedding=embedding,
        collection_name=collection_name,
    )

    retriever = create_retriever(
        vectordb=vectordb,
        search_type=search_type,
        k=k,
    )

    llm = ChatOpenAI(
        model_name=chat_model_name,
        temperature=0,
        api_key=api_key,
    )

    chain = create_chain(
        retriever=retriever,
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
    )

    return RAGService(chain=chain)
