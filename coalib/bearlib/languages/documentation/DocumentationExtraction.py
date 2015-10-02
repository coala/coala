def _get_prefixed_settings(settings, prefix):
    """
    Retrieves all settings with their name matching the given prefix.

    :param settings: The settings dictionary to search in.
    :param prefix:   The prefix all returned settings shall have.
    :return:         A dict with setting-names as keys and setting-values as
                     values.
    """
    return {setting : settings[setting]
            for setting in filter(lambda x: x.startswith(prefix), settings)}
