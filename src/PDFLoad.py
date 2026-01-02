from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
from common.paths import ENV_PATH
from common.prompts import SYSTEM_PROMPT
from preprosessing.source import load_documents
from preprosessing.normalize import normalize_documents
from preprosessing.chunk import chunk_documents
from preprosessing.embed import create_embedding
import os

load_dotenv(ENV_PATH)

# 環境変数の取得
api_key = os.getenv("OPENAI_API_KEY")
embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
chat_model_name = os.getenv("CHAT_MODEL_NAME")

documents = load_documents()

normalized_documents = normalize_documents(documents)

chunked_documents = chunk_documents(normalized_documents)

embeddings = create_embedding(api_key, embedding_model_name)

vectordb = Chroma.from_documents(
    documents=chunked_documents,
    embedding=embeddings,
    collection_name="IRDoc"
)

retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

llm = ChatOpenAI(
    model_name=chat_model_name,
    temperature=0,
    api_key=api_key
)

def format_docs(retrieved_docs):
    """Retriever が返す Document の配列を LLM 用テキストに整形する"""
    return "\n\n".join(d.page_content for d in retrieved_docs)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "【コンテキスト】\n{context}\n\n【質問】\n{input}")
])

output_parser = StrOutputParser()

chain = (
    {
        "context": retriever | RunnableLambda(format_docs), 
        "input": RunnablePassthrough()
    }
    | prompt | llm | output_parser
)

query = "退職金について教えてください。"

result = chain.invoke(query)

print(result)
