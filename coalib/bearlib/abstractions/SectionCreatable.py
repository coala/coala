"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


class SectionCreatable:
    """
    A SectionCreatable is an object that is creatable out of a section object. Thus this is the class for many helper
    objects provided by the bearlib.

    If you want to use an object that inherits from this class the following approach is recommended:
    Instantiate it via the from_section method. You can provide default arguments via the lower case keyword
    arguments. Example:
        SpacingHelper.from_section(section, tabwidth=8)
    creates a SpacingHelper and if the "tabwidth" setting is needed and not contained in section, 8 will be taken.

    In addition you might want to implement the get_non_optional_settings and get_optional_settings method of your bear.
    """
    @classmethod
    def from_section(cls, section, **kwargs):
        """
        Creates the object from a section object.

        :param section: A section object containing at least the settings specified by get_non_optional_settings()
        :param kwargs: defaults for settings with the given key. If no setting with the specified key is needed it will
                       be ignored.
        """
        raise NotImplementedError

    @staticmethod
    def get_non_optional_settings():
        """
        Retrieves the minimal set of settings that need to be defined in order to use this object.

        :return: a dictionary of needed settings as keys and help texts as values
        """
        return {}

    @staticmethod
    def get_optional_settings():
        """
        Retrieves the settings needed IN ADDITION to the ones of get_non_optional_settings to use this object without
        internal defaults.

        :return: a dictionary of needed settings as keys and help texts as values
        """
        return {}
