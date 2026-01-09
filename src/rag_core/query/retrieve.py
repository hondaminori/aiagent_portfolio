from typing import Any, Iterable
from langchain_core.documents import Document
from common.logging_config import logging
from common.logging_config import log_start_end

logger = logging.getLogger(__name__)

@log_start_end
def create_retriever(vectordb: any, search_type: str = "similarity", k: int = 3) -> Any:
    """VectorStore から Retriever を作成する
    Args:
        vectordb: VectorStore のインスタンス
        search_type (str, optional): 検索タイプ. Defaults to 'similarity'.
        k (int, optional): 返すドキュメント数. Defaults to 3.
    Returns:
        Retriever のインスタンス

    vectordbと戻り値は、LangChainのバージョンによって import パスが変わり得るので
    今は無理に固定しないことにした。
    """
    return vectordb.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k}
    )

@log_start_end
def format_retrieved_docs(retrieved_docs: Iterable[Document]) -> str:
    """Retriever が返す Document の配列を LLM 用テキストに整形する
     
    Args:
        retrieved_docs (Iterable[Document]): Retriever が返すドキュメントの配列
        以下のreturnを見ると、単にjoinしているだけなので、Listなどの指定はなく、
        Iterableであれば何でもよい。将来的な互換性を考慮してこのようにした。

    Returns:
        str: 整形されたテキスト
    """
    retrieved_str = "\n\n".join(d.page_content for d in retrieved_docs)
    logging.debug(retrieved_str)

    return retrieved_str