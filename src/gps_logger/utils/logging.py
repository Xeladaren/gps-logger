
import logging

from . import args

def log_type(str):
    if str.isnumeric():
        return int(str)
    elif str in logging.getLevelNamesMapping():
        return logging.getLevelNamesMapping()[str]
    else:
        raise ValueError

def getLogger(name):

    log_level = args.get('log_level')

    if log_level <= logging.DEBUG:
        formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    else:
        formatter = logging.Formatter("[%(levelname)s] %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(stream_handler)
    logger.setLevel(log_level)

    return logger
