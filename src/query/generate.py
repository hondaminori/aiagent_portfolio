from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from query.retrieve import format_retrieved_docs
from typing import Any

def create_prompt(system_prompt: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "【コンテキスト】\n{context}\n\n【質問】\n{input}")
    ])

def create_chain(retriever: Any, llm: Any, system_prompt: str) -> Any:
    prompt = create_prompt(system_prompt)
    output_parser = StrOutputParser()

    return (
        {
            "context": retriever | RunnableLambda(format_retrieved_docs),
            "input": RunnablePassthrough()
        }
        | prompt
        | llm
        | output_parser
    )
