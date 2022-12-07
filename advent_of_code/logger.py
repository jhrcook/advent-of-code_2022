"""Logging in Advent of Code 2022."""

import logging


def _get_console_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    fmt = logging.Formatter(
        "[%(levelname)s] %(asctime)s"
        + " - %(filename)s:%(funcName)s:%(lineno)d\n   %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(fmt)
    return handler


logger = logging.getLogger("AoC2022")
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(_get_console_handler())


def set_console_handler_level(to: int | str) -> None:
    """Set the console handler level.

    Args:
        to (Union[int, str]): New log level for console handlers.

    Returns:
        None: None
    """
    _idx_console_loggers = [0]  #
    for idx in _idx_console_loggers:
        handler = logger.handlers[idx]
        handler.setLevel(to)
