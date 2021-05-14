from coalib.parsing.filters import available_filters


class InvalidFilterException(LookupError):
    def __init__(self, filter_name):
        joined_available_filters = ', '.join(sorted(available_filters))
        super().__init__(
            f'{filter_name!r} is an invalid filter. Available filters:'
            f' {joined_available_filters}')
