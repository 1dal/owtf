"""
owtf.logging
~~~~~~~~~~~~
Helper functions for useful logging (console, file and stream)
"""

import logging
import multiprocessing

from owtf.utils import catch_io_errors
from owtf.config.service import get_log_path


def enable_logging(**kwargs):
    """Enables both file and console logging

        . note::

    + process_name <-- can be specified in kwargs
    + Must be called from inside the process because we are kind of
        overriding the root logger

    :param kwargs: Additional arguments to the logger
    :type kwargs: `dict`
    :return:
    :rtype: None
    """
    process_name = kwargs.get("process_name", multiprocessing.current_process().name)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handler = catch_io_errors(logging.FileHandler)
    file_handler = file_handler(get_log_path(process_name), mode="w+")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(FileFormatter())

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(ConsoleFormatter())

    # Replace any old handlers
    logger.handlers = [file_handler, stream_handler]


def disable_console_logging(**kwargs):
    """Disables console logging

    . note::
        Must be called from inside the process because we should remove handler for that root logger. Since we add
        console handler in the last, we can remove the last handler to disable console logging

    :param kwargs: Additional arguments to the logger
    :type kwargs: `dict`
    :return:
    :rtype: None
    """
    logger = logging.getLogger()
    if isinstance(logger.handlers[-1], logging.StreamHandler):
        logger.removeHandler(logger.handlers[-1])
