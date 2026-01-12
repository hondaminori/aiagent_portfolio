import os
from dotenv import load_dotenv

from common.paths import ENV_PATH
from common.logging_config import setup_logging
from common.config import CHAT_MODEL_NAME, EMBEDDING_MODEL_NAME

def init_app(app_name: str) -> None:
    """
    起動点で必ず最初に呼ぶ初期化。
    - .env 読み込み
    - APP_NAME 設定
    - logging 初期化
    """

    load_dotenv(ENV_PATH)
    os.environ.setdefault("APP_NAME", app_name)

    if not EMBEDDING_MODEL_NAME:
        raise ValueError("定数 EMBEDDING_MODEL_NAME が設定されていません")

    if not CHAT_MODEL_NAME:
        raise ValueError("定数 CHAT_MODEL_NAME が設定されていません")

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("定数 OPENAI_API_KEY (.env) が設定されていません")

    setup_logging()
