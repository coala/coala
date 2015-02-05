def cached_iterator(iterator):
    """
    Decorator for an iterator that should not yield duplications
    :param iterator: python iterator
    :return: python iterator that yields each item only once per call
    """
    def c_iterator(*args, **kwargs):
        yielded = []
        for item in iterator(*args, **kwargs):
            if item in yielded:
                pass
            else:
                yielded.append(item)
                yield item
    return c_iterator