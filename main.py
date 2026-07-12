import logging
import uvicorn

from src.logging_config import setup_logging

logger = logging.getLogger(__name__)


def main():
    setup_logging("INFO")

    logger.info("Starting satellite app")

    # uvicorn.run("src.app:app", host="127.0.0.1", port=8080, reload=True)
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True, log_config=None)


if __name__ == "__main__":
    main()
