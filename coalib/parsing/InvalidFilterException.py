class InvalidFilterException(Exception):
    def __init__(self, filter_name=None, available_filters=None):
        self.filter_name = filter_name
        self.available_filters = available_filters

    def __str__(self):
        res= self.filter_name + ' is an invalid filter. Available filters: ' + self.available_filters
        return res
