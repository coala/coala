from datetime import datetime
from collections import Counter
import json
import io
import logging
import logging.config


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


def configure_logging(color=True):
    """
    Configures the logging with hard coded dictionary.
    """
    import sys

    # reset counter handler
    CounterHandler.reset()

    logging.config.dictConfig({
        'version': 1,
        'handlers': {
            'colored': {
                'class': 'logging.StreamHandler',
                'formatter': 'colored' if color else 'plain',
                'stream': sys.stderr
            },
            'counter': {
                'class': 'coalib.output.Logging.CounterHandler'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['colored', 'counter']
        },
        'formatters': {
            'colored': {
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


def configure_json_logging():
    """
    Configures logging for JSON.
    :return: Returns a ``StringIO`` that captures the logs as JSON.
    """
    stream = io.StringIO()

    # reset counter handler
    CounterHandler.reset()

    logging.config.dictConfig({
        'version': 1,
        'handlers': {
            'json': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'stream': stream
            },
            'counter': {
                'class': 'coalib.output.Logging.CounterHandler'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['json', 'counter']
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
