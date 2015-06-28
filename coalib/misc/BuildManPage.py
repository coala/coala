import datetime
from distutils.core import Command
from distutils.errors import DistutilsOptionError
import argparse


class BuildManPage(Command):
    """
    Add a `build_manpage` command  to your setup.py.
    To use this Command class import the class to your setup.py,
    and add a command to call this class::

        from coalib.misc.BuildManPage import BuildManPage

        setup(
              ...
              ...
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
        try:
            mod = __import__(mod_name, fromlist=fromlist)
            self._parser = \
                getattr(mod, func_name)(formatter_class=ManPageFormatter)

        except ImportError as err:
            raise err

        self.announce('Writing man page %s' % self.output)
        self._today = datetime.date.today()

    def run(self):

        dist = self.distribution
        homepage = dist.get_url()
        appname = self._parser.prog

        sections = {'distribution': ("The latest version of {} may be "
                                     "downloaded from {}".format(appname,
                                                                 homepage))
                    }

        dist = self.distribution
        mpf = ManPageFormatter(appname,
                               desc=dist.get_description(),
                               long_desc=dist.get_long_description(),
                               ext_sections=sections)

        m = mpf.format_man_page(self._parser)

        with open(self.output, 'w') as f:
            f.write(m)


class ManPageFormatter(argparse.HelpFormatter):
    """
    Formatter class to create man pages.
    This class relies only on the parser, and not distutils.
    """
    def __init__(self,
                 prog,
                 indent_increment=2,
                 max_help_position=24,
                 width=None,
                 section=1,
                 desc=None,
                 long_desc=None,
                 ext_sections=None,
                 authors=None,
                 ):

        super(ManPageFormatter, self).__init__(prog)

        self._prog = prog
        self._section = 1
        self._today = datetime.date.today().strftime('%Y\\-%m\\-%d')
        self._desc = desc
        self._long_desc = long_desc
        self._ext_sections = ext_sections

    def _get_formatter(self, **kwargs):
        return self.formatter_class(prog=self.prog, **kwargs)

    @staticmethod
    def _markup(txt):
        return txt.replace('-', '\\-')

    @staticmethod
    def _underline(string):
        return "\\fI\\s-1" + string + "\\s0\\fR"

    @staticmethod
    def _bold(string):
        if not string.strip().startswith('\\fB'):
            string = '\\fB' + string
        if not string.strip().endswith('\\fR'):
            string = string + '\\fR'
        return string

    def _mk_synopsis(self, parser):
        self.add_usage(parser.usage, parser._actions,
                       parser._mutually_exclusive_groups, prefix='')
        usage = self._format_usage(None, parser._actions,
                                   parser._mutually_exclusive_groups, '')

        usage = usage.replace('%s ' % self._prog, '')
        usage = '.SH SYNOPSIS\n \\fB%s\\fR %s\n' \
            % (ManPageFormatter._markup(self._prog), usage)
        return usage

    def _mk_title(self, prog):
        return '.TH {0} {1} {2}\n'.format(prog, self._section,
                                          self._today)

    @staticmethod
    def _make_name(parser):
        return '.SH NAME\n%s \\- %s\n' % (parser.prog,
                                          parser.description)

    def _mk_description(self):
        if self._long_desc:
            long_desc = self._long_desc.replace('\n', '\n.br\n')
            return '.SH DESCRIPTION\n%s\n' % self._markup(long_desc)
        else:
            return ''

    @staticmethod
    def _mk_footer(sections):
        if not hasattr(sections, '__iter__'):
            return ''

        footer = []
        for section, value in sections.items():
            part = ".SH {}\n {}".format(section.upper(), value)
            footer.append(part)

        return '\n'.join(footer)

    def format_man_page(self, parser):
        page = []
        page.append(self._mk_title(self._prog))
        page.append(self._mk_synopsis(parser))
        page.append(self._mk_description())
        page.append(ManPageFormatter._mk_options(parser))
        page.append(ManPageFormatter._mk_footer(self._ext_sections))

        return ''.join(page)

    @staticmethod
    def _mk_options(parser):
        formatter = parser._get_formatter()

        # positionals, optionals and user-defined groups
        for action_group in parser._action_groups:
            formatter.start_section(None)
            formatter.add_text(None)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        # epilog
        formatter.add_text(parser.epilog)

        # determine help from format above
        return '.SH OPTIONS\n' + formatter.format_help()

    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar

        else:
            parts = []

            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(
                    [ManPageFormatter._bold(action_str) \
                     for action_str in action.option_strings])

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            else:
                default = ManPageFormatter._underline(action.dest.upper())
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append('%s %s' % (self._bold(option_string),
                                            args_string))

            return ', '.join(parts)
