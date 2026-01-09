from langchain_community.document_loaders import PyPDFLoader
from common.paths import DOC_DIR
from common.logging_config import logging
from common.logging_config import log_start_end

logger = logging.getLogger(__name__)

@log_start_end
def load_documents():
    """
    PDFファイルからドキュメントを読み込む
    """
    # logger.info("load_documents() を開始します")

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

    for doc in documents:
        _pagecontent_preview = doc.page_content.replace(chr(10), ' ')[:100]
        logger.debug(f"ドキュメント内容の一部: {_pagecontent_preview}...")

    # logger.info("load_documents() を終了します")
    return documents
