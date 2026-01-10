import logging
import os
import datetime


def create_logger():
    try:

        date = datetime.datetime.now().strftime("%Y_%m_%d")
        log_dir = "log"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger("main_log")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        logger.handlers.clear()

        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s',
            datefmt='%Y_%m_%d %H:%M:%S'
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        # logger.addHandler(console_handler)

        file_path = os.path.join(log_dir, f"{date}.log")
        file_handler = logging.FileHandler(file_path, encoding="utf-8", mode="a")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    except Exception as e:
        print(f"Ошибка при создании логгера: {e}")
        return None
