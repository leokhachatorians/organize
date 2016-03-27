import argparse
import textwrap
import sys

class Parser(argparse.ArgumentParser):
    def error(self, error):
        print("\nError: {}".format(error))
        self.print_help()
        sys.exit(1)

parser = Parser(
        prog="organize",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            --------------------------------
            | organize, clean up your mess |
            --------------------------------
                - organize specific extensions into
                    specific folders
                - customizable to your needs
        '''))

sub_parser = parser.add_subparsers(
    dest='choice')

sub_config = sub_parser.add_parser(
    'config',
    help='\
        Bring up the configuration menu to alter organize\
        to fit your needs')

sub_config.add_argument(
    'config',
    action='store_true')
