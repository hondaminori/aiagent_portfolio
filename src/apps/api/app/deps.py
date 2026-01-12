from rag_core.query.service import create_service_from_env

_service = None  # module-level singleton

def init_service() -> None:
    """
    アプリ起動時に1回だけ呼ぶ想定。
    .env を読み込み、RAGService を初期化して保持する。
    """
    global _service

    _service = create_service_from_env()

def get_service():
    """
    ルーターから呼ばれる。初期化済み service を返す。
    """
    if _service is None:
        raise RuntimeError("init_service() が呼ばれていません。")
    return _service
