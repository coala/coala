from datetime import datetime
import json
import io
import logging
import logging.config

from coalib.output.printers.LOG_LEVEL import LOG_LEVEL


def configure_logging(new_log_level=logging.INFO, incremental=False):
    """
    Configures the logging with hard coded dictionary.
    When changing the log_level, the incremental param should be True.
    json-handler are created so that they exist when
    the Log Level is changed via `configure_logging`

    :param new_log_level: The new log level to set for json and console
                          handlers.
    :param incremental: `False` if setting up new loggers, `True` if only
                        changing the log level.

    :return: The new_log_level is returned.
    """
    import sys

    logging.config.dictConfig({
        'version': 1,
        'incremental': incremental,
        'handlers': {
            'console-handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'color',
                'stream': sys.stderr,
                'level': LOG_LEVEL.reverse.get(new_log_level)
            },
            'file-handler': {
                'class': 'logging.FileHandler',
                'formatter': 'no-color',
                'filename': 'coala-log',
                'mode': 'w',
                'level': 'DEBUG'
            },
            'json-handler': {
                'class': 'logging.NullHandler',
                'level': LOG_LEVEL.reverse.get(new_log_level)
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['file-handler', 'console-handler', 'json-handler']
        },
        'formatters': {
            'color': {
                '()': 'colorlog.ColoredFormatter',
                'format': '%(log_color)s[%(levelname)s]%(reset)s[%(asctime)s]'
                          ' %(message)s',
                'datefmt': '%X',
                'log_colors': {
                    'ERROR': 'red',
                    'WARNING': 'yellow',
                    'INFO': 'blue',
                    'DEBUG': 'green'
                }
            },
            'no-color': {
                '()': 'logging.Formatter',
                'format': '[%(levelname)s][%(asctime)s] %(message)s'
            }
        }
    })
    return new_log_level


def configure_json_logging():
    """
    Configures logging for JSON.
    Console-handler and file-handler are created so that they exist when
    the Log Level is changed via `configure_logging`

    :return: Returns a ``StringIO`` that captures the logs as JSON.
    """
    stream = io.StringIO()

    logging.config.dictConfig({
        'version': 1,
        'handlers': {
            'json-handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'stream': stream
            },
            'console-handler': {
                'class': 'logging.NullHandler'
            },
            'file-handler': {
                'class': 'logging.NullHandler'
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['json-handler', 'console-handler', 'file-handler']
        },
        'formatters': {
            'json': {
                '()': 'coalib.output.Logging.JSONFormatter',
            }
        }
    })
    return stream


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for python logging.
    """
    @staticmethod
    def format(record):
        message = {
            'timestamp': datetime.utcfromtimestamp(record.created).isoformat(),
            'message': record.getMessage(),
            'level': record.levelname,
        }
        return json.dumps(message)
