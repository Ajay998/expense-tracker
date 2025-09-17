import logging
import os

def setup_logger(name, log_file='server.log', level=logging.DEBUG):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, log_file)
    logger = logging.getLogger(name)

    logger.setLevel(level)
    file_handler = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger