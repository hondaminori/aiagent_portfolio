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
SEARCH_KWARGS = 3
SEARCH_TYPE = "similarity"

# model
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
CHAT_MODEL_NAME = "gpt-5.1"

# ログ
LOG_LEVEL = "DEBUG"
LOG_DEST = "file" # file / stdout

# 精度向上
SKIP_LEADING_PAGES = 0
