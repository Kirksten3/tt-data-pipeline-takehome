import logging

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Creates and returns a logger with the specified name and log level.

    :param name: Name of the logger.
    :param level: Logging level (default is logging.INFO).
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(ch)

    return logger