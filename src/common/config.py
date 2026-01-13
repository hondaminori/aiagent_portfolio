# .envはアップしてはいけない内容。
# そうではないものはここに書く。

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TEXT_SPLITTER_SEPARATORS = [
    "\n\n",
    "\n",
    "。",
    "、",
    " ",
    ""
]
COLLECTION_NAME = "workrules"

# retriever
SEARCH_KWARGS = 2
SEARCH_TYPE = "similarity"

# model
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
CHAT_MODEL_NAME = "gpt-4o-mini"

# ログ
LOG_LEVEL = "DEBUG"
LOG_DEST = "file" # file / stdout

# 精度向上(-1：除外機能は無効、0が1ページ目)
SKIP_LEADING_PAGES = 0
