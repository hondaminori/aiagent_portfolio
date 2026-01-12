from langchain_openai import OpenAIEmbeddings
from common.logging_config import logging
from common.logging_config import log_start_end
from common.config import EMBEDDING_MODEL_NAME
import os

logger = logging.getLogger(__name__)

@log_start_end
def create_embedding() -> OpenAIEmbeddings:
    """
    OpenAI Embedding オブジェクトを生成する。
    """
    api_key = os.getenv("OPENAI_API_KEY")

    embedding = OpenAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        api_key=api_key
    )

    return embedding
