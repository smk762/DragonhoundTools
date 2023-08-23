#!/usr/bin/env python3
import logging
import os
import sys


class CustomFormatter(logging.Formatter):

    black = "\x1b[30m"
    error = "\x1b[31m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    orange = "\x1b[33m"
    blue = "\x1b[34m"
    purple = "\x1b[35m"
    cyan = "\x1b[36m"
    lightgrey = "\x1b[37m"
    table = "\x1b[37m"
    darkgrey = "\x1b[90m"
    lightred = "\x1b[91m"
    lightgreen = "\x1b[92m"
    yellow = "\x1b[93m"
    lightblue = "\x1b[94m"
    status = "\x1b[94m"
    pink = "\x1b[95m"
    lightcyan = "\x1b[96m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"  # type: ignore
    datefmt = "%d-%b-%y %H:%M:%S"

    FORMATS = {
        logging.DEBUG: f"{lightblue}{format}{reset}",
        logging.INFO: f"{lightgreen}{format}{reset}",
        logging.WARNING: f"{red}{format}{reset}",
        logging.ERROR: f"{lightred}{format}{reset}",
        logging.CRITICAL: f"{bold_red}{format}{reset}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# create logger with project folder name
logging.basicConfig()
logger = logging.getLogger("DragonhoundTools")
logger.setLevel(logging.DEBUG)
logger.propagate = False

# create console handler with a higher log level
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)


if __name__ == "__main__":
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.critical("critical message")
    logger.info(f"logger_app_name: {logger_app_name}")
