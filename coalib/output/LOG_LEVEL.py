class LOG_LEVEL:
    DEBUG = 0
    WARNING = 1
    ERROR = 2

    @staticmethod
    def from_str(string):
        return {
            "debug": LOG_LEVEL.DEBUG,
            "warning": LOG_LEVEL.WARNING,
            "error": LOG_LEVEL.ERROR
        }.get(string.lower(), LOG_LEVEL.WARNING)
