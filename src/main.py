from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
from common.paths import ENV_PATH
from common.prompts import SYSTEM_PROMPT
from preprocessing.source import load_documents
from preprocessing.normalize import normalize_documents
from preprocessing.chunk import chunk_documents
from preprocessing.embed import create_embedding
from preprocessing.vector_backend import build_vectorstore, load_vectorstore
from query.retriever import create_retriever, format_retrieved_docs
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

# vectordb = build_vectorstore(
#     documents=chunked_documents,
#     embedding=embeddings,
#     collection_name="WorkRules"
# )

vectordb = load_vectorstore(
    embedding=embeddings,
    collection_name="WorkRules"
)

retriever = create_retriever(
    vectordb=vectordb,
    search_type="similarity",
    k=3
)

llm = ChatOpenAI(
    model_name=chat_model_name,
    temperature=0,
    api_key=api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "【コンテキスト】\n{context}\n\n【質問】\n{input}")
])

output_parser = StrOutputParser()

chain = (
    {
        "context": retriever | RunnableLambda(format_retrieved_docs), 
        "input": RunnablePassthrough()
    }
    | prompt | llm | output_parser
)

query = "退職金について教えてください。"

result = chain.invoke(query)

print(result)
