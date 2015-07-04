import argparse

from coalib.misc.i18n import _


def dbus_arg_parser(formatter_class=argparse.RawDescriptionHelpFormatter):
    arg_parser = argparse.ArgumentParser(
        formatter_class=formatter_class,
        prog="coala-dbus",
        description=_("coala-dbus is a dbus interface for coala - COde "
                      "AnaLysis Application. Its goal is to provide a dbus API "
                      "to make static code analysis easy and convenient "
                      "for all languages."))

    arg_parser.add_argument('-p',
                            '--persistent',
                            help=_("Keeps the dbus server open even if no "
                                   "clients are connected to it."),
                            action="store_true")
    arg_parser.add_argument('-v',
                            '--verbose',
                            help=_("Prints debugging information"),
                            action="store_true")

    return arg_parser
