from pathlib import Path
import json
import os
import argparse
import sys

__description__ = 'A light performance tools.'
__version__ = '0.1.0'

__BASE_DIR__ = Path(__file__).parent.parent

sys.path.insert(0, str(Path(__file__).parent))


def cwd() -> Path:
    return __BASE_DIR__


def resources(file: str) -> Path:
    return cwd().joinpath('resources', file)


resources_path: str = os.path.join(cwd(), 'resources')


def cli():
    ...


parser = argparse.ArgumentParser(description=__description__, add_help=False, allow_abbrev=False, exit_on_error=True,
                                 epilog='*********************', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {__version__}', help="show version")

parser.add_argument('-v', '--verbose', action='count', default=0)

group = parser.add_argument_group('ThreadGroup')
group.add_argument('-t', '--thread_number', help='one thread means a user', dest='thread_number', default=1, type=int,
                   metavar='user')
group.add_argument('-l', '--loop_count', help='the collection loop count', dest='loop_count', default=1, type=int,
                   metavar='loop')

subparsers = parser.add_subparsers(dest='subCommand', help='subCommand')
parser_a = subparsers.add_parser('run', help='run help')
parser_a.add_argument('-f', '--file', dest='file', metavar='DIR_OR_FILE', type=str, nargs='?',
                      help='specify directory or file')

args = parser.parse_args()
parser.print_help()
print(vars(args))
