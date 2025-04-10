import logging
import sys
from datetime import datetime


def setup_logger():
    # Don't create file handler if we're running tests
    handlers = [logging.StreamHandler()]

    # Only add file handler if not in test environment
    if "pytest" not in sys.modules:
        handlers.append(
            logging.FileHandler(f'app_{datetime.now().strftime("%Y-%m-%d")}.log')
        )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers,
        force=True,
    )

    return logging.getLogger()


logger = setup_logger()
