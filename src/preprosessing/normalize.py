from langchain_core.documents import Document
import re

def normalize_documents(documents: list[Document]) -> list[Document]:
    """
    ソースから取り込んだデータをキレイにする。
     - filter_documents ドキュメントの振り分け（page_contentが空のものを除去する等）
     - clean_documents page_contentの正規化（不要な改行や空白の削除等）

    切り分けは、件数が変わるものは filter_documents、
    page_content のみを変えるものは clean_documents と考える。
    filterが先、cleanが後。理由は件数を削ってから内容を整形した方が効率的だから。

    Args:
        documents (List[Document]): normalize対象のDocumentリスト
    Returns:
        List[Document]: normalizeされたDocumentリスト
    """
    docs = filter_documents(documents)
    docs = clean_documents(docs)

    return docs

def filter_documents(documents: list[Document]) -> list[Document]:
    """
    documentsの振り分け系処理を行う
     - page_contentが空のものを除去する

    Args:
        documents (List[Document]): 振り分け対象のDocumentリスト
    Returns:
        List[Document]: 内容的に問題ないDocumentリスト
    """
    
    filtered_documents = []

    # 内包表記はあえて使っていない
    for doc in documents:
        if doc.page_content and doc.page_content.strip() != "":
            filtered_documents.append(doc)

    return filtered_documents

def clean_documents(documents: list[Document]) -> list[Document]:
    """
    page_contentsの整形系処理を行う。
     - 改行コードの統一
     - 不要な改行の削除
     - 余分な空白の削除
    Args:
        documents (List[Document]): 整形対象のDocumentリスト
    Returns:
        List[Document]: 整形されたDocumentリスト
    """

    cleaned_documents = []

    for doc in documents:
        page_content = doc.page_content.replace('\r\n', '\n').replace('\r', '\n')
        page_content = re.sub(r'(\n[ \t]*){3,}', '\n\n', page_content)
        # 単なるmetadata=doc.metadataでは参照渡しになるため、copy()でコピーを作成してから渡す
        cleaned_documents.append(Document(page_content=page_content, metadata=doc.metadata.copy()))

    return cleaned_documents