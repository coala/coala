import logging
from copy import deepcopy
from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.collecting.Collectors import (
    collect_bears, collect_bears_by_aspects, get_all_bears)


SUPPORTED_LANG_COMB = [{'python', 'jinja2'}]


def get_temp_file_lang(nl_info_dict, temp_file):
    """
    Return the language of the temp created file.
    """
    for file, file_info in nl_info_dict['nl_file_info'].items():
        for lang, temp_file_name in file_info.items():
            if temp_file == temp_file_name:
                return lang


def get_orig_file(nl_info_dict, temp_file):
    """
    Return the original file name for the temp_file
    """
    for file, file_info in nl_info_dict['nl_file_info'].items():
        for lang, temp_file_name in file_info.items():
            if temp_file == temp_file_name:
                return file


def check_lang_support(lang_list):
    """
    Check if the languages supplied by the user is supported by the nested
    language mode of coala.

    :param lang_list: List containing all the nested languages specified by the
                      user.
    """
    lang_supported = False
    lang_list = [lang.lower() for lang in lang_list]
    lang_set = set(lang_list)

    for supported_lang_set in SUPPORTED_LANG_COMB:
        # The combination of the languages are supported if the difference of
        # the set is zero.
        if not supported_lang_set.difference(lang_set):
            lang_supported = True

    if not lang_supported:
        logging.error('The language combination are not supported. ' +
                      'Please check if the languages are provided with' +
                      'the correct names')
        raise SystemExit(2)


def generate_lang_bear_dict(nl_info_dict):
    """
    Map the language with bears specified in the CLI arguments.

    :param nl_info_dict: Dictionary containing the information about the nested
                         language files sepecified by the user.
    :return:             Returns a dictionary with `language` as the key and
                         `bears` as the value.

    For eg, If the user specified that the nested language files has python
    and jinja2 as languages and the bears we want to run is `PEP8Bear`,
    `Jinja2Bear` and `SpaceConsistencyBear`.

    >> nl_info_dict = {}
    >> nl_info_dict['languages'] = ['python', 'jinja2']
    >> nl_info_dict['bears'] = ['PEP8Bear','Jinja2Bear', 'SpaceConsistencyBear']
    >> generate_lang_bear_dict(nl_info_dict)
    {'python':['PEP8Bear','SpaceConsistencyBear'],
    'jinja': ['Jinja2Bear', 'SpaceConsistencyBear']
    }
    """
    lang_bear_dict = {}
    bears = nl_info_dict.get('bears', '')
    bear_dirs = nl_info_dict.get('bear_dirs', None)

    from coalib.settings.Section import Section
    local_bears, global_bears = collect_bears(
        bear_dirs if bear_dirs else Section('').bear_dirs(),
        bears,
        [BEAR_KIND.LOCAL, BEAR_KIND.GLOBAL],
        warn_if_unused_glob=False)

    # Initialze the lang_bear_dict
    for lang in nl_info_dict.get('languages'):
        lang_bear_dict[lang] = []

    # Create a dictionary for local bears and global bears
    for bear in local_bears + global_bears:
        # for bear in bears:

        bear_lang = [lang.lower() for lang in bear.LANGUAGES]

        if 'all' in bear_lang:
            for lang in nl_info_dict.get('languages'):
                lang_bear_dict[lang].append(bear.name)
            continue

        for lang in nl_info_dict.get('languages'):
            if lang in bear_lang:
                lang_bear_dict[lang].append(bear.name)

    return lang_bear_dict


def nl_info_dict(args=None):
    """
    Return a dictionary with the information about nested language file.

    :nl_info_dict: The dictionaray containing all the details

    For eg: If the user passes the following arguments to coala

    ```
    coala --handle-nested --languages=python,jinja2 --files=test.py,test2.py
    --bears=PEP8Bear,SpaceConsistencyBear,Jinja2Bear --settings use_space=True
    ```

    If the above args are passed to nl_info dict, the output we get is:

    >>> nl_info_dict =  {
    ...     'bears': ['PEP8Bear', 'SpaceConsistencyBear', 'GitCommitBear'],
    ...     'files': ['test.py', 'test2.py'],
    ...     'lang_bear_dict': {
    ...                         'jinja2': ['SpaceConsistencyBear'],
    ...                         'python': ['PEP8Bear', 'SpaceConsistencyBear']
    ...                       },
    ...     'languages': ['python', 'jinja2'],
    ... }

    The details of keys in nl_info_dict are,

    :bears:          Bears specified by the user
    :files:          Nested Files to run the analysis on
    :languages:      Languages present in the nested file
    :lang_bear_dict: Dictionary with language as the key and the bear as
                     values

    """
    nl_info_dict = {}
    for arg_key, arg_value in sorted(vars(args).items()):
        if not arg_value:
            continue

        arg_key = str(arg_key).lower().strip()

        if (arg_key == 'files' or arg_key == 'bears' or arg_key == 'languages'
                or arg_key == 'bear_dirs'):
            arg_values = (arg_value[0].strip()).split(',')
            if arg_key == 'languages':
                # In order to avoid the upper and lower case mistakes from user
                # while defining the languages
                arg_values = [lang.lower() for lang in arg_values]
                nl_info_dict[arg_key] = arg_values
            else:
                nl_info_dict[arg_key] = arg_values

    check_lang_support(nl_info_dict['languages'])

    nl_info_dict['lang_bear_dict'] = generate_lang_bear_dict(nl_info_dict)

    return nl_info_dict


def generate_arg_list(args=None):
    """
    Generates seperate argument list for each of the nested language.

    The input to the function is the original arg object that the user passed
    to coala. We make a copy of the original argument object for each of the
    new argument object we make for each language.

    What we do here is just change the values present in the arg.__dict__ this
    makes it look like as if the args have been passed  via the command line.
    Since we cannot regenerate the args as these first scanned by the shell
    and then passed to the python.

    The following values in the args will be changed:

    :key files:  A new temp file name that will be used to store all the lines
                 from a particular language
    :key bears:  The bears that should run for the specific files.

    For eg:

    If the original args passed to coala is,
    ```
    coala --handle-nested --languages=python,jinja2 --files=test.py,test2.py
    --bears=PEP8Bear,SpaceConsistencyBear,Jinja2Bear --settings use_space=True
    ```

    If the above args are passed to generate_arg_list, the output of nl_info we
    get is:

    >>> nl_info =  {
    ...     'bears': ['PEP8Bear', 'SpaceConsistencyBear', 'GitCommitBear'],
    ...     'files': ['test.py', 'test2.py'],
    ...     'lang_bear_dict': {
    ...                         'jinja2': ['SpaceConsistencyBear'],
    ...                         'python': ['PEP8Bear', 'SpaceConsistencyBear']
    ...                       },
    ...     'languages': ['python', 'jinja2'],
    ...     'nl_file_info': { 'test.py' : {
    ...                                     'python' : 'test.py_nl_python',
    ...                                     'jinja2' : 'test.py_nl_jinja2'
    ...                                   },
    ...
    ...                       'test2.py': {
    ...                                     'python' : 'test2.py_nl_python',
    ...                                     'jinja2' : 'test2.py_nl_jinja2'
    ...                                   }
    ...                     }
    ... }

    When the above args are passed to generate_arg_list, it returns the
    following argument objects, which is equivalent to the following

    ```
    coala --files=test.py_nl_python --bears=PEP8Bear,SpaceConsistencyBear
    ```

    ```
    coala --files=test2.py_nl_python --bears=PEP8Bear,SpaceConsistencyBear
    ```

    ```
    coala --files=test.py_nl_jinja2 --bears=Jinja2Bear,SpaceConsistencyBear
    ```

    ```
    coala --files=test.py_nl_jinja2 --bears=Jinja2Bear,SpaceConsistencyBear
    ```
    """
    nl_info = nl_info_dict(args)

    # Initialize nl_file_info dict
    nl_info['nl_file_info'] = {}
    for file in nl_info['files']:
        nl_info['nl_file_info'][file] = {}

    # Generate the arguments for each language
    arg_list = []
    for lang in nl_info['languages']:
        for file in nl_info['files']:
            # Create a new instance of args
            arg_lang = deepcopy(args)
            temp_nl_file = file + '_nl_' + str(lang)

            nl_info['nl_file_info'][file][lang] = temp_nl_file
            arg_lang.__dict__['files'] = temp_nl_file
            arg_lang.__dict__['bears'] = ','.join(
                                            nl_info['lang_bear_dict'][lang])

            arg_list.append(arg_lang)

    return arg_list, nl_info
