from coalib.parsing.filters.decorators import typed_filter


@typed_filter(('bearclass', 'Bear', 'Section'))
def section_tags_filter(section_or_bear, args):
    """
    Filters the bears or sections by ``tags``.

    :param section_or_bear: A section or bear instance on which filtering
                            needs to be carried out.
    :param args:            Set of tags on which it needs to be filtered.
    :return:                ``True`` if this instance matches the criteria
                            inside args, ``False`` otherwise.
    """
    enabled_tags = list(map(str.lower, args))
    if len(enabled_tags) == 0:
        return True

    section = section_or_bear
    if hasattr(section_or_bear, 'section'):
        # If it is a bear or bear like object it has
        # to have an associated section which contains
        # all settings, including tags.
        section = section_or_bear.section

    section_tags = section.get('tags', False)
    if str(section_tags) == 'False':
        return False

    section_tags = map(str.lower, section_tags)
    return bool(set(section_tags) & set(enabled_tags))
