from datetime import datetime
import json
import io
import logging
import logging.config


def configure_logging():
    """
    Configures the logging with hard coded dictionary.
    """
    import sys

    logging.config.dictConfig({
        'version': 1,
        'handlers': {
            'colored': {
                'class': 'logging.StreamHandler',
                'formatter': 'colored',
                'stream': sys.stderr
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['colored']
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
            }
        }
    })


def configure_json_logging():
    """
    Configures logging for JSON.
    :return: Returns a ``StringIO`` that captures the logs as JSON.
    """
    stream = io.StringIO()

    logging.config.dictConfig({
        'version': 1,
        'handlers': {
            'json': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'stream': stream
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['json']
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
