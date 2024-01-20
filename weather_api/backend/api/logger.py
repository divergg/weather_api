import logging

logger = logging.getLogger()
STREAM_HANDLER = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s]\t%(levelname)2s:\t%(message)s")
STREAM_HANDLER.setFormatter(
    formatter
)
FILE_HANDLER = logging.FileHandler('./api/logs/main_api.log')
FILE_HANDLER.setFormatter(formatter)
logger.addHandler(STREAM_HANDLER)
logger.addHandler(FILE_HANDLER)
logger.setLevel("DEBUG")