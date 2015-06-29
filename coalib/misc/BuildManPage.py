import datetime
import argparse


class ManPageFormatter(argparse.HelpFormatter):
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
        return ManPageFormatter._add_format(string, "\\fI", "\\fR")

    @staticmethod
    def _bold(string):
        return ManPageFormatter._add_format(string, "\\fB", "\\fR")

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
        usage = '.SH SYNOPSIS\n \\fB%s\\fR %s\n' \
            % (ManPageFormatter._markup(self._prog), usage)
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
        for section, value in sections.items():
            part = ".SH {}\n {}".format(section.upper(), value)
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
