import os
import sys
import logging

import requests
from genericpath import exists
from appdirs import user_data_dir

from coalib.misc import Constants
from coalib.output.ConfWriter import ConfWriter
from coalib.settings.ConfigurationGathering import load_configuration
from coalib.settings.Setting import Setting


class ConfigGenerator:
    """
    This class generates a .coafile
    """

    def __init__(self, args):
        self.args = args
        self.collector_file = Constants.local_coafile
        self.base_url = ('https://raw.githubusercontent.com/PrajwalM2212/'
                         'coala-styles/master/coala_styles/styles/')

    def download_cached_file(self, url, filename):
        """
        Download the config file or return the existing config
        file if it already exists.

        :param url: The url to download from
        :param filename: The filename in which the config will be saved
        :return: Return filename
        """
        filename = os.path.join(self.data_dir, filename)
        if exists(filename):
            return filename

        response = requests.get(url, stream=True, timeout=20)
        response.raise_for_status()

        with open(filename, 'ab') as file:
            for chunk in response.iter_content(125):
                file.write(chunk)
        return filename

    @property
    def data_dir(self):
        """
        Define the path where downloaded config files will be stored.

        :return: data_dir path
        """
        data_dir = os.path.abspath(os.path.join(
            user_data_dir('coala-styles')))

        os.makedirs(data_dir, exist_ok=True)
        return data_dir

    def save_sections(self, sections):
        """
        Saves the given sections if they are to be saved.

        :param sections: A section dict.
        """

        conf_writer = ConfWriter(Constants.local_coafile)
        conf_writer.write_sections(sections)
        conf_writer.close()

    def create_coafile(self):
        """
        Generate .coafile based on user preferences.

        Downloads the config files if they don't already
        exist. Combines the style-based config files
        and writes them into .coafile.
        """
        config_groups = self.args.generate_config
        file_list = []
        lint_files_dict = {}

        for config_group in config_groups:
            config_group_args = config_group.split(':')
            try:
                files = '**'
                excludes = ''
                num_args = len(config_group_args)
                if num_args == 2:
                    lang, author = config_group_args
                    lint_files_dict[lang] = (files, excludes)
                elif num_args == 3:
                    lang, author, files = config_group_args
                    lint_files_dict[lang] = (files, excludes)
                else:
                    lang, author, files, excludes = config_group_args
                    lint_files_dict[lang] = (files, excludes)
            except ValueError:
                logging.error('Supply command line args in '
                              'the form language:style_name:files:excludes ')
                sys.exit(255)

            try:
                file_name = (self.download_cached_file(
                    (self.base_url + '{}/{}_config.coafile')
                    .format(lang, author),
                    lang + '_' + author))

                file_list.append(file_name)

            except requests.exceptions.HTTPError:
                logging.warning('{} style guide for {} not avilable'.format(
                    author, lang
                ))

        with open(self.collector_file, 'a') as outfile:
            for fname in file_list:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

        self.args.save = True
        self.args.config = self.collector_file

        sections, targets = load_configuration(None, None,
                                               args=self.args)

        sections.get('cli').delete_setting('config')
        sections.get('cli').delete_setting('generate_config')

        sections['cli'].name = 'all'
        sections['all'] = sections['cli']
        del sections['cli']

        for lang, (files, excludes) in lint_files_dict.items():
            if sections.get(lang, None):
                sections.get(lang).append(Setting('files', files))
                sections.get(lang).append(Setting('ignore', excludes))
                sections[lang].name = 'all.{}'.format(lang)
                sections['all.{}'.format(lang)] = sections[lang]
                del sections[lang]

        for name, section in sections.items():
            section.append(Setting('comment1', '', ))

        self.save_sections(sections)
