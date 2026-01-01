from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
from common.paths import DOC_DIR, ENV_PATH
from common.prompts import SYSTEM_PROMPT
from common.config import CHUNK_SIZE, CHUNK_OVERLAP, TEXT_SPLITTER_SEPARATORS
import os

load_dotenv(ENV_PATH)

# 環境変数の取得
api_key = os.getenv("OPENAI_API_KEY")
embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
chat_model_name = os.getenv("CHAT_MODEL_NAME")

pdf_paths = sorted(DOC_DIR.glob("*.pdf"))

documents = []

for pdf_path in pdf_paths:
    loader = PyPDFLoader(str(pdf_path))
    documents.extend(loader.load())

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=TEXT_SPLITTER_SEPARATORS
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
