import logging
import os
import datetime

"""Модуль для логирования проекта"""


def create_logger():
    try:
        date = datetime.datetime.now().strftime("%Y_%m_%d")
        log_dir = "log"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        message_format = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s'
        )
        logger = logging.getLogger("main_log")
        # logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(message_format)
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(
            f"{log_dir}/{date}.log",
            encoding="utf-8",
            mode="a"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(message_format)
        logger.addHandler(file_handler)

        return logger
    except Exception as e:
        logging.error(e)