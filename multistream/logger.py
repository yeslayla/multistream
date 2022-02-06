import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

def enable_debug_logger() -> None:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)