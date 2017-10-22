from __future__ import print_function

import argparse
import pprint
import sys

import six

from week_parser.base import parse_week


class PrettyPrinter(pprint.PrettyPrinter):
    """
    A PrettyPrinter that normalizes the output of Python2 unicode strings and
    Python3 strings.

    In order to ensure that Python2 and Python3 produce the same output when
    dealing with non-ascii characters, we need to decode the strings and
    represent them between single quotes.
    """

    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, six.binary_type) or hasattr(obj, 'decode'):
            obj = obj.decode('UTF-8').replace("'", "\\'")
            return (six.u("'{}'").format(obj), True, False)
        return pprint.PrettyPrinter.format(self, obj,
                                           context, maxlevels, level)


parser = argparse.ArgumentParser(description='WeekParser utility')
parser.add_argument(dest='filename', type=str, help='Input CSV file')


def get_options(args):
    return parser.parse_args(args)


def main(args=None):
    """
    The parser entrypoint

    If it gets called without arguments argparse will use 'sys.argv'.
    """
    args = get_options(args)
    try:
        result = parse_week(args.filename)
        printer = PrettyPrinter(width=120)
        printer.pprint(result)
    except IOError as exc:
        print(exc.strerror, file=sys.stderr)
    except ValueError as exc:
        print('Invalid file format: {}'.format(exc), file=sys.stderr)


if __name__ == '__main__':
    main()
