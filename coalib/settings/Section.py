from collections import OrderedDict
import copy

from coalib.output.printers.FilePrinter import FilePrinter
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.NullPrinter import NullPrinter
from coalib.output.ConsoleInteractor import ConsoleInteractor, ConsolePrinter
from coalib.output.Interactor import Interactor
from coalib.misc.i18n import _
from coalib.settings.Setting import Setting


class Section:
    """
    This class holds a set of settings.
    """

    @staticmethod
    def __prepare_key(key):
        return str(key).lower().strip()

    def __init__(self,
                 name,
                 defaults=None,
                 interactor=ConsoleInteractor(),
                 log_printer=ConsolePrinter()):
        if defaults is not None and not isinstance(defaults, Section):
            raise TypeError("defaults has to be a Section object or None.")
        if defaults is self:
            raise ValueError("defaults may not be self for non-recursivity.")
        if not isinstance(interactor, Interactor):
            raise TypeError("The interactor parameter has to be of type "
                            "Interactor.")
        if not isinstance(log_printer, LogPrinter):
            raise TypeError("The log_printer parameter has to be of type "
                            "LogPrinter.")

        self.name = str(name)
        self.defaults = defaults
        self.contents = OrderedDict()
        self.interactor = interactor
        self.log_printer = log_printer

    def retrieve_logging_objects(self):
        """
        Creates an appropriate log printer and interactor according to the
        settings.
        """
        log_type = str(self.get("log_type", "console")).lower()
        str_log_level = str(self.get("log_level", "")).upper()
        log_level = LOG_LEVEL.str_dict.get(str_log_level, LOG_LEVEL.WARNING)

        if log_type == "console":
            self.log_printer = ConsolePrinter(log_level=log_level)
        else:
            try:
                # ConsolePrinter is the only printer which may not throw an
                # exception (if we have no bugs though) so well fallback to him
                # if some other printer fails
                if log_type == "none":
                    self.log_printer = NullPrinter()
                else:
                    self.log_printer = FilePrinter(filename=log_type,
                                                   log_level=log_level)
            except:
                self.log_printer = ConsolePrinter(log_level=log_level)
                self.log_printer.log(
                    LOG_LEVEL.WARNING,
                    _("Failed to instantiate the logging method '{}'. Falling "
                      "back to console output.").format(log_type))

        # We currently only offer console interactor, so we'll ignore the
        # output setting for now
        self.interactor = ConsoleInteractor.from_section(
            self,
            log_printer=self.log_printer)

    def append(self, setting, custom_key=None):
        if not isinstance(setting, Setting):
            raise TypeError
        if custom_key is None:
            key = self.__prepare_key(setting.key)
        else:
            key = self.__prepare_key(custom_key)

        # Setting asserts key != "" for us
        self.contents[key] = setting

    def add_or_create_setting(self,
                              setting,
                              custom_key=None,
                              allow_appending=True):
        """
        Adds the value of the setting to an existing setting if there is
        already a setting  with the key. Otherwise creates a new setting.
        """
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
            # Since we only return the iterator of joined (which doesnt contain
            # values) it's ok to override values here
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
        value_list = ", ".join(key + " : " + str(self.contents[key])
                               for key in self.contents)
        return self.name + " {" + value_list + "}"

    def get(self, key, default="", ignore_defaults=False):
        """
        Retrieves the item without raising an exception. If the item is not
        available an appropriate Setting will be generated from your provided
        default value.

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
        :return: a deep copy of this object, with the exception of the
        log_printer and the interactor
        """
        result = copy.copy(self)
        result.contents = copy.deepcopy(self.contents)
        if self.defaults is not None:
            result.defaults = self.defaults.copy()

        return result

    def update(self, other_section, ignore_defaults=False):
        """
        Incorporates all keys and values from the other section into this one.
        Values from the other section override the ones from this one.

        Default values from the other section override the default values from
        this only.

        :param other_section: Another Section
        :param ignore_defaults: If set to true, do not take default values from
        other
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
