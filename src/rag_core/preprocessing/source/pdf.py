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
    if not DOC_DIR.exists():
        logger.error(f"ドキュメント格納ディレクトリ {DOC_DIR} が存在しません")
        raise FileNotFoundError(f"ドキュメント格納ディレクトリ {DOC_DIR} が存在しません")
    
    pdf_paths = sorted(DOC_DIR.glob("*.pdf"))

    if not pdf_paths:
        logger.warning(f"{DOC_DIR} にPDFファイルが見つかりません")
        raise FileNotFoundError(f"{DOC_DIR} にPDFファイルが見つかりません")

    documents = []

    for pdf_path in pdf_paths:
        try:
            logger.info(f"PDFファイルを読み込みます: {pdf_path}")
            loader = PyPDFLoader(str(pdf_path))
            documents.extend(loader.load())
        except Exception as e:
            logger.error(f"PDFファイルの読み込みに失敗しました: {pdf_path} | error: {e}")

    logger.info(f"{len(pdf_paths)} 本のPDFファイルから {len(documents)} 件のドキュメントを読み込みました。")

    if logger.isEnabledFor(logging.DEBUG):
        for doc in documents:
            _pagecontent_preview = doc.page_content.replace(chr(10), ' ')[:100]
            logger.debug(f"PDFから取得した内容: {_pagecontent_preview}...")

    return documents
