import logging
from logging.handlers import WatchedFileHandler
import socket
from os import getenv
from time import gmtime


LOG_LEVEL: str = getenv("ARTIFACTS_LOG_LEVEL", "INFO")
LOG_FILE: str = getenv("ARTIFACTS_LOG_FILE", "python_artifacts.log")
LOG_LEVELS: dict[str, int] = {"INFO": logging.INFO, "DEBUG": logging.DEBUG}


def init_logger() -> None:
    """
    Initialises the logging functionality, should be used when you make a script to do actions on the mmo and not on any of the modules
    """
    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setLevel(LOG_LEVELS[LOG_LEVEL])

    file_handler: WatchedFileHandler = WatchedFileHandler(LOG_FILE)

    logging.basicConfig(
        format=f"%(asctime)s.%(msecs)03dz {socket.gethostname()} %(levelname).1s %(name)-18s %(message)s",
        datefmt="%Y-%m-%dT%H:ML%S",
        level=LOG_LEVELS[LOG_LEVEL],
        handlers=[stream_handler, file_handler],
    )
    logging.Formatter.converter = gmtime


def create_logger(module_name: str) -> logging.Logger:
    """Creates logger for module to be used to track messages on the script

    Args:
        module_name (str): artifacts_requests

    Returns:
        logging.Logger: A configured logging module
    """
    return logging.getLogger(module_name)
