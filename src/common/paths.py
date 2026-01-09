from pathlib import Path
import os

def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Project root (pyproject.toml) が見つかりません")

PROJECT_ROOT = find_project_root(Path(__file__))
DOC_DIR = PROJECT_ROOT / "docs"
ENV_PATH = PROJECT_ROOT / "config" / ".env"
CHROMA_PERSIST_DIR = PROJECT_ROOT / "db" / "chroma_db"
LOG_DIR = PROJECT_ROOT / "logs"
