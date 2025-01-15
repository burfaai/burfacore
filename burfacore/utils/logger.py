import sys
import traceback
import logging
from datetime import datetime
from logging import Logger
from pathlib import Path

path = Path(__file__)
_logger = logging.getLogger(__name__)


class BurfaLogger:
    """_summary_"""

    def __init__(self, logger: Logger = _logger) -> None:
        self.current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logger = logger

        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        self.file_handler = logging.FileHandler(
            f"{path.parent.name}/.logs/{self.current_time}"
        )
        self.file_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(logging.DEBUG)

    def get_logger(self):
        """_summary_"""
        sys.excepthook = self._handler
        return self.logger

    def _handler(self, exctype, value, tb):
        self.logger.exception(f"Uncaught exception: {value}")
        self.logger.exception("".join(traceback.format_exception(exctype, value, tb)))
