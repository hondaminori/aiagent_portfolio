from langchain_community.document_loaders import PyPDFLoader
from common.paths import DOC_DIR, ENV_PATH

def load_documents():
    pdf_paths = sorted(DOC_DIR.glob("*.pdf"))

    documents = []

    for pdf_path in pdf_paths:
        loader = PyPDFLoader(str(pdf_path))
        documents.extend(loader.load())

    return documents