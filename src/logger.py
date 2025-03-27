import logging
import logging.config
import os
import sys

from .config import LOG_DIR, LOGGING

def setup_logger():
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
    except OSError as e:
        print(f"Critical error: {e}", file=sys.stderr)
        sys.exit(1)

    logging.config.dictConfig(LOGGING)