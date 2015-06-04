from coalib.misc.DictUtilities import inverse_dicts


def show_bears(local_bears, global_bears, show_bears_callback):
    """
    Extracts all the bears from each enabled section or the sections in the
    targets and passes a dictionary to the show_bears_callback method.

    :param local_bears:         Dictionary of local bears with section names
                                as keys and bear list as values.
    :param global_bears:        Dictionary of global bears with section
                                names as keys and bear list as values.
    :param show_bears_callback: The callback that is used to print these
                                bears. It will get one parameter holding
                                bears as key and the list of section names
                                where it's used as values.
    """
    bears = inverse_dicts(local_bears, global_bears)

    show_bears_callback(bears)
