class InvalidFilterException(Exception):
    def __init__(self, filter_name, available_filters):
        super().__init__('{!r} is an invalid filter. Available filters: {}'
                         .format(filter_name,
                                 ', '.join(sorted(available_filters))))
