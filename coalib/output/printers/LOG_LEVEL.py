import logging

from coalib.misc.Enum import enum


LOG_LEVEL = enum(DEBUG=logging.DEBUG,
                 INFO=logging.INFO,
                 WARNING=logging.WARNING,
                 ERROR=logging.ERROR)
LOG_LEVEL_COLORS = {LOG_LEVEL.ERROR: 'red',
                    LOG_LEVEL.WARNING: 'yellow',
                    LOG_LEVEL.INFO: 'blue',
                    LOG_LEVEL.DEBUG: 'green'}
LOG_LEVEL_TO_LOGGING_LEVEL = {LOG_LEVEL.ERROR: logging.ERROR,
                              LOG_LEVEL.WARNING: logging.WARNING,
                              LOG_LEVEL.INFO: logging.INFO,
                              LOG_LEVEL.DEBUG: logging.DEBUG}
