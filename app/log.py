import logging
import sys
from typing import Optional

LOGGING_FORMATTER = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

DEBUG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR']


def get_logger(
    name: Optional[str] = None,
    level: str = 'DEBUG'
) -> logging.Logger:

    logger = logging.getLogger(name=name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(LOGGING_FORMATTER)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if not level or level not in DEBUG_LEVELS:
        logger.warning(
            'Invalid logging level %s. Setting logging level to DEBUG.', level
        )
        level = 'DEBUG'

    logger.setLevel(level=level)
    return logger
