import logging
import functools


@functools.cache
def getLogger(name=None):
    logger = logging.getLogger(name=name)
    stdio = logging.StreamHandler()
    logger.addHandler(stdio)
    return logger
