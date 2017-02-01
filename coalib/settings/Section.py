import copy
import os
import sys
from collections import OrderedDict

from coalib.collecting.Collectors import collect_registered_bears_dirs
from coala_utils.decorators import enforce_signature, generate_repr
from coala_utils.string_processing import unescape
from coalib.misc.DictUtilities import update_ordered_dict_key
from coalib.settings.Setting import Setting, path_list
from coalib.parsing.Globbing import glob_escape


def append_to_sections(sections,
                       key,
                       value,
                       origin,
                       section_name=None,
                       from_cli=False,
                       to_append=False):
    """
    Appends the given data as a Setting to a Section with the given name. If
    the Section does not exist before it will be created empty.

    :param sections:     The sections dictionary to add to.
    :param key:          The key of the setting to add.
    :param value:        The value of the setting to add.
    :param origin:       The origin value of the setting to add.
    :param section_name: The name of the section to add to.
    :param from_cli:     Whether or not this data comes from the CLI.
    :param to_append:    The boolean value if setting value needs to be
                         appended to a setting in the defaults of a section.
    """
    if key == '' or value is None:
        return

    if section_name == '' or section_name is None:
        section_name = 'default'

    if not section_name.lower() in sections:
        sections[section_name.lower()] = Section(section_name)

    sections[section_name.lower()].append(Setting(
        key, str(value), origin, from_cli=from_cli, to_append=to_append))


@generate_repr()
class Section:
    """
    This class holds a set of settings.

    To add settings and sections to a dictionary of sections we can use
    ``append_to_sections``:

    >>> sections = {}
    >>> append_to_sections(sections,
    ...                    'test1',
    ...                    'val',
    ...                    'origin',
    ...                    section_name='all')
    >>> 'all' in sections
    True
    >>> len(sections)
    1
    >>> str(sections)
    "{'all': <Section object(contents=OrderedDict([('test1', ..."

    We can also add settings that can be appended to other settings. Basically
    it takes the default value of the setting which resides in the defaults of
    the section and appends the value of the setting in the second and returns
    the value of the setting:

    >>> append_to_sections(sections,
    ...                    'test1',
    ...                    'val2',
    ...                    'origin',
    ...                    section_name='all.python',
    ...                    to_append=True)

    When the section has no defaults:

    >>> str(sections['all.python']['test1'])
    'val2'

    After assigning defaults:

    >>> sections['all.python'].set_default_section(sections)
    >>> str(sections['all.python']['test1'])
    'val, val2'
    """

    @staticmethod
    def __prepare_key(key):
        return str(key).lower().strip()

    def __init__(self,
                 name,
                 defaults=None):
        if defaults is not None and not isinstance(defaults, Section):
            raise TypeError('defaults has to be a Section object or None.')
        if defaults is self:
            raise ValueError('defaults may not be self for non-recursivity.')

        self.name = str(name)
        self.defaults = defaults
        self.contents = OrderedDict()

    def bear_dirs(self):
        bear_dirs = path_list(self.get('bear_dirs', ''))
        for bear_dir in bear_dirs:
            sys.path.append(bear_dir)
        bear_dir_globs = [
            os.path.join(glob_escape(bear_dir), '**')
            for bear_dir in bear_dirs]
        bear_dir_globs += [
            os.path.join(glob_escape(bear_dir), '**')
            for bear_dir in collect_registered_bears_dirs('coalabears')]
        return bear_dir_globs

    def is_enabled(self, targets):
        """
        Checks if this section is enabled or, if targets is not empty, if it is
        included in the targets list.

        :param targets: List of target section names, all lower case.
        :return:        True or False
        """
        if len(targets) == 0:
            return bool(self.get('enabled', 'true'))

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
            val.value = str(val._value) + '\n' + setting._value
            self.append(val, custom_key=key)
        else:
            self.append(setting, custom_key=key)

    @enforce_signature
    def __setitem__(self, key: str, value: (str, Setting)):
        """
        Creates a Setting object from the given value if needed and assigns the
        setting to the key:

        >>> section = Section('section_name')
        >>> section['key'] = 'value'
        >>> section['key'].value
        'value'

        :param key:   Argument whose value is to be set
        :param value: The value of the given key
        :return:      Returns nothing.
        """
        if isinstance(value, Setting):
            self.append(value, custom_key=key)
        else:  # It must be a string since signature is enforced
            self.append(Setting(key, value))

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
        if key == '':
            raise IndexError('Empty keys are invalid.')

        res = copy.deepcopy(self.contents.get(key, None))
        if res is not None:
            if res.to_append and self.defaults and res.key in self.defaults:
                res.value = self.defaults[key]._value + ', ' + res._value
                res.to_append = False
                return res
            res.to_append = False
            return res

        if self.defaults is None or ignore_defaults:
            raise IndexError('Required index is unavailable.')

        return self.defaults[key]

    def __str__(self):
        value_list = ', '.join(key + ' : ' + repr(str(self[key]))
                               for key in self.contents)
        return self.name + ' {' + value_list + '}'

    def get(self, key, default='', ignore_defaults=False):
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
            raise TypeError('other_section has to be a Section')

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

    def set_default_section(self, sections, section_name=None):
        """
        Find and set the defaults of a section from a dictionary of sections.
        The defaults are found on the basis of '.' in section names:

        >>> sections = {'all': Section('all')}
        >>> section = Section('all.python')
        >>> section.set_default_section(sections)
        >>> section.defaults.name
        'all'
        >>> section = Section('all.python.syntax')
        >>> section.set_default_section(sections)
        >>> section.defaults.name
        'all'

        :param sections:     A dictionary of sections.
        :param section_name: Optional section name argument to find the default
                             section for. If not given then use member section
                             name.
        """
        default_section = '.'.join((section_name or self.name).split('.')[:-1])

        if default_section:
            if default_section in sections:
                self.defaults = sections[default_section]
            else:
                self.set_default_section(sections, default_section)
        elif 'cli' in sections and self.name.lower() != 'cli':
            # CLI section is now default
            self.defaults = sections['cli']
