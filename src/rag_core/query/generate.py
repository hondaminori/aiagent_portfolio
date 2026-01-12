from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from rag_core.query.retrieve import format_retrieved_docs
from common.logging_config import log_start_end
from typing import Any

@log_start_end
def create_prompt(system_prompt: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "【コンテキスト】\n{context}\n\n【質問】\n{input}")
    ])

@log_start_end
def create_chain(retriever: Any, llm: Any, system_prompt: str) -> Any:
    prompt = create_prompt(system_prompt)
    output_parser = StrOutputParser()

    # 1. まずコンテキストを取得する部分を定義
    retrieval_step = {
        "context": retriever, # ここではまだフォーマットせず、Documentオブジェクトのまま保持
        "input": RunnablePassthrough()
    }

    # 2. 回答を生成する部分を定義
    # assign を使うことで、元の辞書に "answer" というキーを追加できる
    return retrieval_step | RunnablePassthrough.assign (
        answer = 
        # promptに渡す直前に context を文字列にフォーマットする
            {"context": lambda x: format_retrieved_docs(x["context"]), "input": lambda x: x["input"]}
            | prompt
            | llm
            | output_parser
        )
    
