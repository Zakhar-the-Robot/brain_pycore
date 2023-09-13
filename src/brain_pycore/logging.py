# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

from enum import IntEnum
import logging
import os

CONFIG_LOG_FORMAT = "%(relativeCreated)8d [%(levelname).1s] %(name)-s:  %(message)s"
CONFIG_DONT_PRINT_TO_FILES = False
CONFIG_LOG_DIR = "zakhar/logs"


class LOG_LEVEL(IntEnum):
    CRITICAL = logging.CRITICAL
    FATAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


def new_logger(name, log_level=LOG_LEVEL.INFO):

    logger = logging.getLogger(name=name)
    formatter = logging.Formatter(CONFIG_LOG_FORMAT)
    # stream
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if not CONFIG_DONT_PRINT_TO_FILES:
        if not os.path.exists(CONFIG_LOG_DIR):
            os.makedirs(CONFIG_LOG_DIR)
        # file
        handler = logging.FileHandler(f"{CONFIG_LOG_DIR}/{name}.log")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # union file
        handler = logging.FileHandler(f"{CONFIG_LOG_DIR}/full.log")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(log_level)
    return logger


log = new_logger(name="Common Log")

if __name__ == '__main__':
    log.error("test")
    log.warning("test")
