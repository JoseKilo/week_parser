from __future__ import print_function

import argparse
import sys
from pprint import pprint

from week_parser.base import parse_week


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
        pprint(result)
    except IOError as exc:
        print(exc.strerror, file=sys.stderr)
    except ValueError as exc:
        print('Invalid file format: {}'.format(exc), file=sys.stderr)


if __name__ == '__main__':
    main()
