from collections import OrderedDict
import copy

from coalib.misc.Decorators import generate_repr
from coalib.settings.Setting import Setting
from coalib.misc.DictUtilities import update_ordered_dict_key


def append_to_sections(sections,
                       key,
                       value,
                       origin,
                       section_name=None,
                       from_cli=False):
    """
    Appends the given data as a Setting to a Section with the given name. If
    the Section does not exist before it will be created empty.

    :param sections:     The sections dictionary to add to.
    :param key:          The key of the setting to add.
    :param value:        The value of the setting to add.
    :param origin:       The origin value of the setting to add.
    :param section_name: The name of the section to add to.
    :param from_cli:     Whether or not this data comes from the CLI.
    """
    if key == '' or value is None:
        return

    if section_name == "" or section_name is None:
        section_name = "default"

    if not section_name.lower() in sections:
        sections[section_name.lower()] = Section(section_name)

    sections[section_name.lower()].append(
        Setting(key, str(value), origin, from_cli=from_cli))


@generate_repr()
class Section:
    """
    This class holds a set of settings.
    """

    @staticmethod
    def __prepare_key(key):
        return str(key).lower().strip()

    def __init__(self,
                 name,
                 defaults=None):
        if defaults is not None and not isinstance(defaults, Section):
            raise TypeError("defaults has to be a Section object or None.")
        if defaults is self:
            raise ValueError("defaults may not be self for non-recursivity.")

        self.name = str(name)
        self.defaults = defaults
        self.contents = OrderedDict()

    def is_enabled(self, targets):
        """
        Checks if this section is enabled or, if targets is not empty, if it is
        included in the targets list.

        :param targets: List of target section names, all lower case.
        :return:        True or False
        """
        if len(targets) == 0:
            return bool(self.get("enabled", "true"))

        return self.name.lower() in targets

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

        :param key:             The key of the setting to return.
        :param default:         The default value
        :param ignore_defaults: Whether or not to ignore the default section.
        :return:                The setting.
        """
        try:
            return self.__getitem__(key, ignore_defaults)
        except IndexError:
            return Setting(key, str(default))

    def copy(self):
        """
        :return: a deep copy of this object
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

        :param other_section:   Another Section
        :param ignore_defaults: If set to true, do not take default values from
                                other
        :return:                self
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

    def update_setting(self,
                       key,
                       new_key=None,
                       new_value=None):
        """
        Updates a setting with new values.
        :param key:       The old key string.
        :param new_key:   The new key string.
        :param new_value: The new value for the setting
        """
        if new_key is not None:
            self.contents[key].key = new_key
            self.contents = update_ordered_dict_key(self.contents,
                                                    key,
                                                    new_key)
        if new_value is not None:
            if new_key is not None:
                self.contents[new_key].value = new_value
            else:
                self.contents[key].value = new_value

    def delete_setting(self, key):
        """
        Delete a setting
        :param key: The key of the setting to be deleted
        """
        del self.contents[key]
