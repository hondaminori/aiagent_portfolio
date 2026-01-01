from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from common.paths import DOC_DIR, ENV_PATH
import os

load_dotenv(ENV_PATH)

# 環境変数の取得
api_key = os.getenv("OPENAI_API_KEY")
embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
chat_model_name = os.getenv("CHAT_MODEL_NAME")
chunk_size = int(os.getenv("CHUNK_SIZE"))
chunk_overlap = int(os.getenv("CHUNK_OVERLAP"))
text_splitter_separators = os.getenv("TEXT_SPLITTER_SEPARATORS")

pdf_paths = sorted(DOC_DIR.glob("*.pdf"))

documents = []

for pdf_path in pdf_paths:
    loader = PyPDFLoader(str(pdf_path))
    documents.extend(loader.load())

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    separators=text_splitter_separators
)

docs = recursive_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(
    model=embedding_model_name,
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
    model_name=chat_model_name,
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



"""
＜メモ＞



"""
