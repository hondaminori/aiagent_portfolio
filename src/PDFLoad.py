from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[1] / "config" / ".env"
load_dotenv(env_path)
api_key = os.getenv("OPENAI_API_KEY")

main_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(main_path)

files = [f for f in os.listdir('../doc') if os.path.isfile(os.path.join('../doc', f))]

documents = []

for file in files:
    loader = PyPDFLoader(os.path.join('../doc', file))
    documents.extend(loader.load())

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", "。", "、", " ", ""]
)

docs = recursive_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    api_key=api_key
)

vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="IRDoc"
)

count = vectordb._collection.count()

retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
    api_key=api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "与えられた質問に対して、以下のコンテキストを使用して回答してください。コンテキスト:{context}"),
    ("human", "{input}")
])


output_parser = StrOutputParser()

chain = (
    {"context": retriever, "input": RunnablePassthrough()}
    | prompt | llm | output_parser
)

query = "退職金について教えてください。"

result = chain.invoke(query)

print(result)