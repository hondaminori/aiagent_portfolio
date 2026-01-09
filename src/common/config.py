# .envに置けないものはここで定義する。
# 違いは.envでは単なる文字列になってしまうので、それを防ぐため

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

# retriever関連
SEARCH_KWARGS = 100
SEARCH_TYPE = "similarity"