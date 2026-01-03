# 今後データソースを追加することを想定して
# コメントで入れておく。CSVを追加する場合を想定。

from .pdf import load_documents as load_pdf
# from .csv import load_documents as load_csv

def load_documents():
    docs = []
    docs.extend(load_pdf())
    # docs.extend(load_csv())
    return docs

__all__ = ["load_documents"]