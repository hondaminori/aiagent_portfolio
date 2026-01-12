from common.bootstrap import init_app
from common.logging_config import log_start_end
from rag_core.query.service import create_service_from_env
import logging

init_app("ragtest")

logger = logging.getLogger(__name__)

@log_start_end
def main() -> None:
    service = create_service_from_env()

    q = "時短について教えてください。"
    logger.info(f"query: {q}")
    response = service.ask(q)
    logger.info("質問に返答しました")
    logger.info(f"回答: {response["answer"]}")

    if logger.isEnabledFor(logging.DEBUG):
        for source_document in response["source_documents"]:
            content = source_document.page_content.replace('\r\n', ' ').replace('\n', ' ')
            logger.debug(f"判断根拠や参照箇所: {content}" )

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("ragtestが失敗しました")
        raise
