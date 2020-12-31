# *************************************************************************
#
# Copyright (c) 2020 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

import logging
import os

CONFIG_LOG_FORMAT = "%(relativeCreated)8d [%(levelname).1s] %(name)-s:  %(message)s"
CONFIG_DONT_PRINT_TO_FILES = True


def get_logger(name, log_level=logging.INFO):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logger = logging.getLogger(name=name)
    formatter = logging.Formatter(CONFIG_LOG_FORMAT)
    # stream
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if not CONFIG_DONT_PRINT_TO_FILES:
        # file
        handler = logging.FileHandler("logs/" + name + '.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # union file
        handler = logging.FileHandler("logs/" + 'zk.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(log_level)
    return logger
