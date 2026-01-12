"""
service.py

UI（CLI / FastAPI / Streamlit）から呼び出す窓口。
- 起動時に依存物（embedding / vectordb / retriever / chain）を組み立てて保持する
- 問い合わせは ask(query) だけに統一する
"""

from dataclasses import dataclass
from typing import Any, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
from common.telemetry import measure_time_decorator
from rag_core.preprocessing.embed import create_embedding
from rag_core.preprocessing.vector_backend import load_vectorstore
from rag_core.query.retrieve import create_retriever
from rag_core.query.generate import create_chain
from common.logging_config import log_start_end
from common.prompts import SYSTEM_PROMPT
from common.config import EMBEDDING_MODEL_NAME, COLLECTION_NAME, SEARCH_TYPE, SEARCH_KWARGS, CHAT_MODEL_NAME
import os

class RAGResponse(TypedDict):
    query: str
    answer: str
    source_documents: list[Any]

@dataclass
class RAGService:
    """RAG 問い合わせ用サービス（UI非依存）"""
    chain: Runnable

    @measure_time_decorator(label="関数askの実行時間")
    def ask(self, query: str) -> RAGResponse:
        """質問を受け取り回答を返す（UIからはこれだけ呼ぶ）"""
        result = self.chain.invoke(query)
        return {
            "query": query,
            "answer": result["answer"],
            "source_documents": result.get("context", [])
        }

@log_start_end
def create_service_from_env() -> RAGService:
    """
    common.config等で得た設定値から RAGService を組み立てる。
    FastAPI/Streamlitでは「起動時に1回」呼ぶ想定。
    """
    api_key = os.getenv("OPENAI_API_KEY")

    embedding = create_embedding(api_key, EMBEDDING_MODEL_NAME)

    vectordb = load_vectorstore(
        embedding=embedding,
        collection_name=COLLECTION_NAME
    )

    retriever = create_retriever(
        vectordb=vectordb
    )

    llm = ChatOpenAI(
        model_name=CHAT_MODEL_NAME,
        temperature=0,
        api_key=api_key,
    )

    chain = create_chain(
        retriever=retriever,
        llm=llm,
        system_prompt=SYSTEM_PROMPT
    )

    return RAGService(chain=chain)
