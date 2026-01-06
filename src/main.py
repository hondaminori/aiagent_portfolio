from dotenv import load_dotenv
from common.paths import ENV_PATH
from rag_core.query.service import create_service_from_env
from common.logging_config import get_logger
import os


load_dotenv(ENV_PATH)

logger = get_logger(__name__)
logger.info("アプリ起動")

service = create_service_from_env(
    api_key=os.getenv("OPENAI_API_KEY"),
    embedding_model_name=os.getenv("EMBEDDING_MODEL_NAME"),
    chat_model_name=os.getenv("CHAT_MODEL_NAME"),
    collection_name="WorkRules",
    k=3,
    search_type="similarity",
)

print(service.ask("育休について教えてください。"))
