from coalib.parsing.filters import available_filters


class InvalidFilterException(LookupError):
    def __init__(self, filter_name):
        super().__init__('{!r} is an invalid filter. Available filters: {}'
                         .format(filter_name,
                                 ', '.join(sorted(available_filters))))
