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


class SettingsCreatable:
    """
    A SettingsCreatable is an object that is creatable out of a settings object. Thus this is the class for many helper
    objects provided by the bearlib.

    If you want to use an object that inherits from this class the following approach is recommended:
    Instantiate it via the from_settings method. You can provide default arguments via the lower case keyword
    arguments. Example:
        SpacingHelper.from_settings(settings, tabwidth=8)
    creates a SpacingHelper and if the "tabwidth" setting is needed and not contained in settings, 8 will be taken.

    In addition you might want to implement the get_needed_settings method of your bear in the following manner
    (exemplary):
        def get_get_needed_settings():
            needed_settings = {}  # Get your needed settings

            # Retrieve minimal needed settings from SpacingHelper and add them to the dict
            needed_settings.update(SpacingHelper.get_get_minimal_needed_settings())
            return needed_settings

    If you don't want to rely on any defaults you can get a dict of all settings needed by the object via:
        SpacingHelper.get_get_needed_settings()

    Please consider that it is usually good to guess settings for the user if it is possible to do a reasonable guess
    that suits most needs.
    """
    @staticmethod
    def from_settings(settings, **kwargs):
        """
        Creates the object from a settings object.

        :param settings: A settings object containing at least the settings specified by get_minimal_needed_settings()
        :param kwargs: defaults for settings with the given key. If no setting with the specified key is needed it will
                       be ignored.
        """
        raise NotImplementedError

    @staticmethod
    def get_minimal_needed_settings():
        """
        Retrieves the minimal set of settings that need to be defined in order to use this object.

        :return: a dictionary of needed settings as keys and help texts as values
        """
        return {}

    @staticmethod
    def get_needed_settings():
        """
        Retrieves the settings needed to use this object without using defaults.

        :return: a dictionary of needed settings as keys and help texts as values
        """
        raise NotImplementedError
