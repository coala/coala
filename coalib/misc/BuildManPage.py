import argparse
import datetime
from distutils.core import Command
from distutils.errors import DistutilsOptionError


class BuildManPage(Command):
    """
    Add a ``build_manpage`` command  to your setup.py.
    To use this Command class add a command to call this class::

        # For setuptools
        setup(
              entry_points={
                "distutils.commands": [
                    "build_manpage = coalib.misc.BuildManPage:BuildManPage"
                ]
              }
        )

        # For distutils
        from coalib.misc.BuildManPage import BuildManPage
        setup(
              cmdclass={'build_manpage': BuildManPage}
        )

    You can then use the following setup command to produce a man page::

        $ python setup.py build_manpage --output=coala.1 \
            --parser=coalib.parsing.DefaultArgParser:default_arg_parser

    If automatically want to build the man page every time you invoke
    your build, add to your ```setup.cfg``` the following::

        [build_manpage]
        output = <appname>.1
        parser = <path_to_your_parser>
    """
    user_options = [
        ('output=', 'O', 'output file'),
        ('parser=', None, 'module path to an ArgumentParser instance'
         '(e.g. mymod:func, where func is a method or function which return'
         'an arparse.ArgumentParser instance.'),
    ]

    def initialize_options(self):
        self.output = None
        self.parser = None

    def finalize_options(self):
        if self.output is None:
            raise DistutilsOptionError('\'output\' option is required')
        if self.parser is None:
            raise DistutilsOptionError('\'parser\' option is required')
        mod_name, func_name = self.parser.split(':')
        fromlist = mod_name.split('.')
        mod = __import__(mod_name, fromlist=fromlist)
        self._parser = (
            getattr(mod, func_name)(formatter_class=ManPageFormatter))

        self.announce('Writing man page %s' % self.output)
        self._today = datetime.date.today()

    def run(self):
        dist = self.distribution
        homepage = dist.get_url()
        maintainer = dist.get_maintainer()
        _license = dist.get_license()
        appname = self._parser.prog

        sections = {'see also': ('Online documentation: {}'.format(homepage)),
                    'maintainer(s)': maintainer,
                    'license': _license}

        dist = self.distribution
        mpf = ManPageFormatter(appname,
                               desc=dist.get_description(),
                               long_desc=dist.get_long_description(),
                               ext_sections=sections,
                               parser=self._parser)

        formatted_man_page = mpf.format_man_page()

        with open(self.output, 'w') as man_file:
            man_file.write(formatted_man_page)


class ManPageFormatter(argparse.HelpFormatter):

    def __init__(self,
                 prog,
                 indent_increment=2,
                 max_help_position=24,
                 width=None,
                 desc=None,
                 long_desc=None,
                 ext_sections=None,
                 parser=None):
        argparse.HelpFormatter.__init__(self, prog)

        self._prog = prog
        self._section = 1
        self._today = datetime.date.today().strftime('%Y\\-%m\\-%d')
        self._desc = desc
        self._long_desc = long_desc
        self._ext_sections = ext_sections
        self._parser = parser

    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar

        else:
            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts = [ManPageFormatter._bold(action_str)
                         for action_str in action.option_strings]

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            else:
                default = ManPageFormatter._underline(action.dest.upper())
                args_string = self._format_args(action, default)
                parts = ['%s %s' % (self._bold(option_string), args_string)
                         for option_string in action.option_strings]

            return ', '.join(parts)

    @staticmethod
    def _markup(string):
        return string.replace('-', '\\-')

    @staticmethod
    def _add_format(string, front, back):
        if not string.strip().startswith(front):
            string = front + string
        if not string.strip().endswith(back):
            string = string + back
        return string

    @staticmethod
    def _underline(string):
        return ManPageFormatter._add_format(string, '\\fI', '\\fR')

    @staticmethod
    def _bold(string):
        return ManPageFormatter._add_format(string, '\\fB', '\\fR')

    def _mk_title(self):
        return '.TH {0} {1} {2}\n'.format(self._prog,
                                          self._section,
                                          self._today)

    def _mk_name(self):
        return '.SH NAME\n%s\n' % (self._parser.prog)

    def _mk_synopsis(self):
        self.add_usage(self._parser.usage,
                       self._parser._actions,
                       self._parser._mutually_exclusive_groups,
                       prefix='')
        usage = self._format_usage(None,
                                   self._parser._actions,
                                   self._parser._mutually_exclusive_groups,
                                   '')

        usage = usage.replace('%s ' % self._prog, '')
        usage = ('.SH SYNOPSIS\n \\fB%s\\fR %s\n'
                 % (ManPageFormatter._markup(self._prog), usage))
        return usage

    def _mk_description(self):
        if self._long_desc:
            long_desc = self._long_desc.replace('\n', '\n.br\n')
            return '.SH DESCRIPTION\n%s\n' % self._markup(long_desc)
        else:
            return ''

    def _mk_options(self):
        formatter = self._parser._get_formatter()

        # positionals, optionals and user-defined groups
        for action_group in self._parser._action_groups:
            formatter.start_section(None)
            formatter.add_text(None)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        # epilog
        formatter.add_text(self._parser.epilog)

        # determine help from format above
        return '.SH OPTIONS\n' + formatter.format_help()

    def _mk_footer(self):
        sections = self._ext_sections
        if not hasattr(sections, '__iter__'):
            return ''

        footer = []

        for section in sorted(sections.keys()):
            part = '.SH {}\n {}'.format(section.upper(), sections[section])
            footer.append(part)

        return '\n'.join(footer)

    def format_man_page(self):
        page = []
        page.append(self._mk_title())
        page.append(self._mk_name())
        page.append(self._mk_synopsis())
        page.append(self._mk_description())
        page.append(self._mk_options())
        page.append(self._mk_footer())

        return ''.join(page)
