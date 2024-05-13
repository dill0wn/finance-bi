import logging
import functools


@functools.cache
def getLogger():
    logger = logging.getLogger()
    stdio = logging.StreamHandler()
    logger.addHandler(stdio)
    return logger
