from coalib.parsing.filters.Filter import filter


@filter
def can_fix_filter(bear, args):
    """
    Filters the bears by ``CAN_FIX``.

    :param bear: Bear object.
    :param args: Set of fixable issue types on which ``bear`` is to be
                 filtered.
    :return:     ``True`` if this bear matches the criteria inside args,
                 ``False`` otherwise.
    """
    return bool({fix.lower() for fix in bear.CAN_FIX} & args)
