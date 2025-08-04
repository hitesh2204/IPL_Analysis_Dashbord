# logger.py
import logging
import os
from datetime import datetime

def setup_logger(name=__name__):
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_filename = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".log"
    log_path = os.path.join(log_dir, log_filename)

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(name)s:%(lineno)d - %(message)s",
    )

    return logging.getLogger(name)
