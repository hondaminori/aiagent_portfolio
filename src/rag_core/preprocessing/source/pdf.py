from langchain_community.document_loaders import PyPDFLoader
from common.paths import DOC_DIR
from common.logging_config import get_logger

# logger = get_logger(__name__)

import logging
logger = logging.getLogger(__name__)

def load_documents():
    """
    PDFファイルからドキュメントを読み込む
    """

    if not DOC_DIR.exists():
        logger.error(f"ドキュメント格納ディレクトリが存在しません: {DOC_DIR}")
        raise FileNotFoundError(f"ドキュメント格納ディレクトリが存在しません: {DOC_DIR}")
    
    pdf_paths = sorted(DOC_DIR.glob("*.pdf"))

    if not pdf_paths:
        logger.warning(f"DOC_DIR にPDFファイルが見つかりません: {DOC_DIR}")
        raise FileNotFoundError(f"DOC_DIR にPDFファイルが見つかりません: {DOC_DIR}")

    documents = []

    for pdf_path in pdf_paths:
        try:
            logger.info(f"PDFファイルを読み込みます: {pdf_path}")
            loader = PyPDFLoader(str(pdf_path))
            documents.extend(loader.load())
        except Exception as e:
            logger.error(f"PDFファイルの読み込みに失敗しました: {pdf_path} | error: {e}")

    logger.info(f"{len(pdf_paths)} 本のPDFファイルから {len(documents)} 件のドキュメントを読み込みました。")
    return documents
