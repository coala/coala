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
from collections import OrderedDict
import copy
from coalib.output.ConsoleOutputter import ConsoleOutputter, ConsolePrinter, Outputter
from coalib.output.FilePrinter import FilePrinter
from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.output.LogPrinter import LogPrinter
from coalib.misc.i18n import _
from coalib.output.NullPrinter import NullPrinter
from coalib.settings.Setting import Setting


class Section:
    """
    This class holds a set of settings.
    """

    @staticmethod
    def __prepare_key(key):
        return str(key).lower().strip()

    def __init__(self, name, defaults=None, outputter=ConsoleOutputter(), log_printer=ConsolePrinter()):
        if defaults is not None and not isinstance(defaults, Section):
            raise TypeError("defaults has to be a Section object or None.")
        if defaults is self:
            raise ValueError("defaults may not be self for non-recursivity.")
        if not isinstance(outputter, Outputter):
            raise TypeError("The outputter parameter has to be of type Outputter.")
        if not isinstance(log_printer, LogPrinter):
            raise TypeError("The log_printer parameter has to be of type LogPrinter.")

        self.name = str(name)
        self.defaults = defaults
        self.contents = OrderedDict()
        self.outputter = outputter
        self.log_printer = log_printer

    def retrieve_log_printer(self):
        """
        Creates an appropriate log printer according to the 'log_type' setting.
        """
        log_type = str(self.get("log_type", "console")).lower()

        if log_type == "console":
            self.log_printer = ConsolePrinter()
        else:
            try:
                # ConsolePrinter is the only printer which may not throw an exception (if we have no bugs though)
                # so well fallback to him if some other printer fails
                if log_type == "none":
                    self.log_printer = NullPrinter()
                else:
                    self.log_printer = FilePrinter(log_type)
            except:
                self.log_printer = ConsolePrinter()
                self.log_printer.log(LOG_LEVEL.WARNING, _("Failed to instantiate the logging method '{}'. Falling back "
                                                          "to console output.").format(log_type))

    def append(self, setting, custom_key=None):
        if not isinstance(setting, Setting):
            raise TypeError
        if custom_key is None:
            key = self.__prepare_key(setting.key)
        else:
            key = self.__prepare_key(custom_key)

        # Setting asserts key != "" for us
        self.contents[key] = setting

    def _add_or_create_setting(self, setting, custom_key=None, allow_appending=True):
        if custom_key is None:
            key = setting.key
        else:
            key = custom_key

        if self.__contains__(key, ignore_defaults=True) and allow_appending:
            val = self[key]
            val.value = str(val.value) + "\n" + setting.value
        else:
            self.append(setting, custom_key=key)

    def __iter__(self, ignore_defaults=False):
        joined = self.contents.copy()
        if self.defaults is not None and not ignore_defaults:
            # Since we only return the iterator of joined (which doesnt contain values) it's ok to override values here
            joined.update(self.defaults.contents)

        return iter(joined)

    def __contains__(self, item, ignore_defaults=False):
        try:
            self.__getitem__(item, ignore_defaults)

            return True
        except IndexError:
            return False

    def __getitem__(self, item, ignore_defaults=False):
        key = self.__prepare_key(item)
        if key == "":
            raise IndexError("Empty keys are invalid.")

        res = self.contents.get(key, None)
        if res is not None:
            return res

        if self.defaults is None or ignore_defaults:
            raise IndexError("Required index is unavailable.")

        return self.defaults[key]

    def __str__(self):
        return self.name + " {" + ", ".join(key + " : " + str(self.contents[key]) for key in self.contents) + "}"

    def get(self, key, default="", ignore_defaults=False):
        """
        Retrieves the item without raising an exception. If the item is not available an appropriate Setting will be
        generated from your provided default value.

        :param key: The key of the setting to return.
        :param default: The default value
        :param ignore_defaults: Whether or not to ignore the default section.
        :return: The setting.
        """
        try:
            return self.__getitem__(key, ignore_defaults)
        except IndexError:
            return Setting(key, str(default))

    def copy(self):
        """
        :return: a deep copy of this object, with the exception of the log_printer and the outputter
        """
        result = copy.copy(self)
        result.contents = copy.deepcopy(self.contents)
        if self.defaults is not None:
            result.defaults = self.defaults.copy()

        return result

    def update(self, other_section, ignore_defaults=False):
        """
        Incorporates all keys and values from the other section into this one. Values from the other section override
        the ones from this one.

        Default values from the other section override the default values from this only.

        :param other_section: Another Section
        :param ignore_defaults: If set to true, do not take default values from other
        :return: self
        """
        if not isinstance(other_section, Section):
            raise TypeError("other_section has to be a Section")

        self.contents.update(other_section.contents)

        if not ignore_defaults and other_section.defaults is not None:
            if self.defaults is None:
                self.defaults = other_section.defaults.copy()
            else:
                self.defaults.update(other_section.defaults)

        return self
