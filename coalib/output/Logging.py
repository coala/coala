from datetime import datetime
import io
import json
import logging
import logging.config

from coalib.output.printers.LOG_LEVEL import LOG_LEVEL


def configure_logging(log_level=logging.INFO, incremental=False):
    """
    Configures the logging with hard coded dictionary.

    If the incremental param is ``True``, all the log-handlers configuration
    other than level will be ignored.
    Thus, use it only when changing the log_level.
    To change log level with this function, it has to be called once with
    ``incremental=False``.

    :param log_level:
        The log level to set for json and console handlers.
    :param incremental:
        ``False`` if setting up new loggers, ``True`` if only changing
        the log level.
    :return:
        The log_level is returned.
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
                'level': LOG_LEVEL.reverse.get(log_level)
            },
            'json-handler': {
                'class': 'logging.NullHandler',
                'level': LOG_LEVEL.reverse.get(log_level)
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console-handler', 'json-handler']
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
    return log_level


def configure_json_logging():
    """
    Configures logging for JSON.

    NOTE: Use ``configure_logging`` to change log level even if the handler
    is created by ``configure_json_logging``.

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
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['json-handler', 'console-handler']
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
