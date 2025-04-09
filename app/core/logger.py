import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'app_{datetime.now().strftime("%Y-%m-%d")}.log'),
    ],
)

logger = logging.getLogger()
