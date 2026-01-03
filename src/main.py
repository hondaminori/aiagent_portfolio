from dotenv import load_dotenv
import os

from common.paths import ENV_PATH
from query.service import create_service_from_env

load_dotenv(ENV_PATH)

service = create_service_from_env(
    api_key=os.getenv("OPENAI_API_KEY"),
    embedding_model_name=os.getenv("EMBEDDING_MODEL_NAME"),
    chat_model_name=os.getenv("CHAT_MODEL_NAME"),
    collection_name="WorkRules",
    k=3,
    search_type="similarity",
)

print(service.ask("退職金について教えてください。"))
