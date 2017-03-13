import io
import json
import logging
import logging.config
from datetime import datetime
from collections import Counter

from coalib.output.printers.LOG_LEVEL import LOG_LEVEL

class CounterHandler(logging.Handler):
    """
    A logging handler which counts the number of calls
    for each logging level.
    """
    _call_counter = Counter()

    @classmethod
    def reset(cls):
        """
        Reset the counter to 0 for all levels
        """
        cls._call_counter.clear()

    @classmethod
    def emit(cls, record):
        cls._call_counter[record.levelname] += 1

    @classmethod
    def get_num_calls_for_level(cls, level):
        """
        Returns the number of calls registered for a given log level.
        """
        return cls._call_counter[level]


def configure_logging(log_level=logging.INFO, incremental=False,
                      stdout=False, color=True):
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
    :param stdout:
        If ``True`` the logging is done on stdout, else it's done on stderr.
    :param color:
        If ``True`` the logging uses ``color`` formatter, else it uses
        the ``no-color`` formatter.
    :return:
        The new_log_level is returned.

    >>> from coalib.output.Logging import configure_logging
    >>> import logging
    >>> import sys
    >>> configure_logging(stdout=True, color=False)
    20
    >>> logging.info("This world doesn’t belong to them")
    [INFO][...] This world doesn’t belong to them

    We will now change the level to ``ERROR``.

    >>> configure_logging(logging.ERROR, incremental=True)
    40
    >>> logging.info("it belongs to us.")
    >>> logging.error("These violent delights have violent ends.")
    [ERROR][...] These violent delights have violent ends.
    """
    import sys

    # reset counter handler
    CounterHandler.reset()

    logging.config.dictConfig({
        'version': 1,
        'incremental': incremental,
        'handlers': {
            'console-handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'colored' if color else 'plain',
                'stream': sys.stderr if stdout else sys.stderr,
                'level': LOG_LEVEL.reverse.get(log_level)

            },
            'counter-handler': {
                'class': 'coalib.output.Logging.CounterHandler'
            },
            'json-handler': {
                'class': 'logging.NullHandler',
                'level': LOG_LEVEL.reverse.get(log_level)
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console-handler', 'json-handler', 'counter-handler']
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
            'plain': {
                'format': '[%(levelname)s][%(asctime)s] %(message)s',
                'datefmt': '%X',
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

    # reset counter handler
    CounterHandler.reset()

    logging.config.dictConfig({
        'version': 1,
        'handlers': {
            'json-handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'stream': stream
            },
            'counter-handler': {
                'class': 'coalib.output.Logging.CounterHandler'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['json-handler', 'console-handler', 'counter-handler']
            'console-handler': {
                'class': 'logging.NullHandler'
            },
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
