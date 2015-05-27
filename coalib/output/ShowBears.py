from coalib.misc.DictUtilities import inverse_dicts


def show_bears(sections, local_bears, global_bears, show_bears):
    """
    Extracts all the bears from each enabled section or the sections in the
    targets and passes a dictionary to show_bears method of the interactor to
    present the bears to you.

    :param sections     : A dictionary of Sections.
    :param local_bears  : Dictionary of local bears with section names as keys
                          and bear list as values.
    :param global_bears : Dictionary of global bears with section names as keys
                          and bear list as values.
    :param show_bears   : The interactor function show_bears that is used to
                          print these bears
    """
    bears = inverse_dicts(local_bears, global_bears)

    show_bears(bears)
