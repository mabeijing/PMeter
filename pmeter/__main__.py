from pathlib import Path
import argparse
import sys

__description__ = 'A light performance tools.'
__version__ = '0.1.0'

__BASE_DIR__ = Path(__file__).parent.parent

sys.path.insert(0, str(Path(__file__).parent))


def resources(file: str) -> Path:
    return __BASE_DIR__.joinpath('resources', file)


resources_path: Path = __BASE_DIR__.joinpath('resources')

parser = argparse.ArgumentParser(description=__description__, add_help=True, allow_abbrev=False, exit_on_error=True,
                                 epilog='*********************', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {__version__}', help="show version")

subparsers = parser.add_subparsers(dest='subCommand', help='subCommand', title='subCommand')
parser_run = subparsers.add_parser('run', help='run testcase with pytest.')
parser_run.add_argument('-v', '--verbose', action='count', default=0, help='show more detail.')
parser_run.add_argument(dest='file', metavar='DIR_OR_FILE', nargs='?', help='specify directory or file',
                        default=resources_path)

group = parser.add_argument_group('ThreadGroup')
group.add_argument('-t', '--thread_number', help='one thread means a user', dest='thread_number', default=1, type=int,
                   metavar='user')
group.add_argument('-l', '--loop_count', help='the collection loop count', dest='loop_count', default=1, type=int,
                   metavar='loop')

args, extra_args = parser.parse_known_args()

print(args, extra_args)
print(args.subCommand)
file = args.file

if not Path(file).is_absolute():
    print(__BASE_DIR__.joinpath('resources', file))

if __BASE_DIR__.joinpath('resources', file).is_file():
    print('file')
elif __BASE_DIR__.joinpath('resources', file).is_dir():
    print('dir')
else:
    print('33')
