def configure_logging():
    """
    Configures the logging with hard coded dictionary.
    """
    import sys
    import logging.config

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
