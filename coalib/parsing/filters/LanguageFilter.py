from coalib.parsing.filters.Filter import filter


@filter
def language_filter(bear, args):
    """
    Filters the bears by ``LANGUAGES``.

    :param bear: Bear object.
    :param args: Set of languages on which ``bear`` is to be filtered.
    :return:     ``True`` if this bear matches the criteria inside args,
                 ``False`` otherwise.
    """
    return bool({lang.lower() for lang in bear.LANGUAGES} & (args | {'all'}))
