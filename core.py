import logging

import settings

_logger = logging.getLogger(settings.LOG_NAME)
_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
_sHandle = logging.StreamHandler()
_sHandle.setLevel(getattr(logging, settings.LOG_LEVEL))
_sHandle.setFormatter(logging.Formatter(settings.LOG_FORMATTER))
_logger.addHandler(_sHandle)
if hasattr(settings, "LOG_FILE"):
    log_file = getattr(settings, "LOG_FILE")
    fHandle = logging.FileHandler(log_file)
    fHandle.setLevel(getattr(logging, settings.LOG_LEVEL))
    fHandle.setFormatter(logging.Formatter(settings.LOG_FORMATTER))
    _logger.addHandler(fHandle)


def get_logger():
    return _logger
