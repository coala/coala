from coalib.parsing.filters.Filter import filter


@filter
def can_detect_filter(bear, args):
    """
    Filters the bears by ``CAN_DETECT``.

    :param bear: Bear object.
    :param args: Set of detectable issue types on which ``bear`` is to be
                 filtered.
    :return:     ``True`` if this bear matches the criteria inside args,
                 ``False`` otherwise.
    """
    return bool({detect.lower() for detect in bear.CAN_DETECT} & args)
