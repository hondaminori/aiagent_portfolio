from langchain_openai import OpenAIEmbeddings

from common.logging_config import logging
from common.logging_config import log_start_end

logger = logging.getLogger(__name__)

@log_start_end
def create_embedding(api_key: str, embedding_model_name: str) -> OpenAIEmbeddings:
    """
    OpenAI Embedding オブジェクトを生成する。
    """
    embedding = OpenAIEmbeddings(
        model=embedding_model_name,
        api_key=api_key
    )

    return embedding
