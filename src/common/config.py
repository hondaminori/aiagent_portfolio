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
