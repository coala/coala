def unique_iterating(iterator):
    """
    Decorator to make an iterator not yield duplications.

    :param iterator: Any iterator
    :return: An iterator that does not yield results more than one time.
    """
    def unique_iterator(*args, **kwargs):
        yielded = []
        for item in iterator(*args, **kwargs):
            if item in yielded:
                pass
            else:
                yielded.append(item)
                yield item

    return unique_iterator
