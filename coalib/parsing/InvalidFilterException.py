class InvalidFilterException(Exception):

    def __init__(self, filter_name, available_filters):
        self.filter_name = filter_name
        self.available_filters = available_filters
        if self.available_filters is None:
            message = 'Invalid Filter'

        if self.available_filters is not None:
            message = 'Invalid filter. Available filters are : ' + \
                     ' ,'.join(self.available_filters)

        else:
            message = self.filter_name + \
                      ' is an invalid filter. Available filters: ' + \
                      ' ,'.join(self.available_filters)
        super().__init__(message)
