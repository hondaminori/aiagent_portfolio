from pathlib import Path
import os

def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Project root (pyproject.toml) not found.")

PROJECT_ROOT = find_project_root(Path(__file__))

DOC_DIR = PROJECT_ROOT / "docs"
ENV_PATH = PROJECT_ROOT / "config" / ".env"
CHROMA_PERSIST_DIR = PROJECT_ROOT / "db" / "chroma_db"

"""
ログ出力先は、.envの設定を最優先とし、未定義の場合は
プロジェクトルート直下のlogsディレクトリを使用する。
※環境ごと（本番、ローカルなど）にログ出力先を変更するため
"""
DEFAULT_LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR = Path(
    os.getenv("LOG_DIR", DEFAULT_LOG_DIR)
).resolve()