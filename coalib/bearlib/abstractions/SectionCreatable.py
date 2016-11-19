from coalib.settings.FunctionMetadata import FunctionMetadata


class SectionCreatable:
    """
    A SectionCreatable is an object that is creatable out of a section object.
    Thus this is the class for many helper objects provided by the bearlib.

    If you want to use an object that inherits from this class the following
    approach is recommended: Instantiate it via the from_section method. You
    can provide default arguments via the lower case keyword arguments.

    Example:

    ::

        SpacingHelper.from_section(section, tabwidth=8)

    creates a SpacingHelper and if the "tabwidth" setting is needed and not
    contained in section, 8 will be taken.

    It is recommended to write the prototype of the __init__ method according
    to this example:

    ::

        def __init__(self, setting_one: int, setting_two: bool=False):
            pass  # Implementation

    This way the get_optional_settings and the get_non_optional_settings method
    will extract automatically that:

    -  setting_one should be an integer
    -  setting_two should be a bool and defaults to False

    If you write a documentation comment, you can use :param to add
    descriptions to your parameters. These will be available too automatically.
    """

    def __init__(self):
        pass  # Method needs to be available

    @classmethod
    def from_section(cls, section, **kwargs):
        """
        Creates the object from a section object.

        :param section: A section object containing at least the settings
                        specified by get_non_optional_settings()
        :param kwargs:  Additional keyword arguments
        """
        kwargs.update(cls.get_metadata().create_params_from_section(section))

        return cls(**kwargs)

    @classmethod
    def get_metadata(cls):
        return FunctionMetadata.from_function(cls.__init__, omit={'self'})

    @classmethod
    def get_non_optional_settings(cls):
        """
        Retrieves the minimal set of settings that need to be defined in order
        to use this object.

        :return: a dictionary of needed settings as keys and help texts as
                 values
        """
        return cls.get_metadata().non_optional_params

    @classmethod
    def get_optional_settings(cls):
        """
        Retrieves the settings needed IN ADDITION to the ones of
        get_non_optional_settings to use this object without internal defaults.

        :return: a dictionary of needed settings as keys and help texts as
                 values
        """
        return cls.get_metadata().optional_params
