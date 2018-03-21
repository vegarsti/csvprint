import argparse
import sys
import csv
from itertools import islice
from parse_types import *

def create():
    script_name = 'csvprint'
    parser = argparse.ArgumentParser(
        description='Command line utility for pretty printing csv files.',
        formatter_class=argparse.RawTextHelpFormatter,
        prog=script_name,
    )
    parser.add_argument(
        'filename',
        type=str,
        help='file to pretty print',
        nargs='?',
    )
    parser.add_argument(
        '-s',
        '--separator',
        default=',',
        help="separator/delimiter used in csv file\ndefault is comma\nuse 'tab' for tab separated files\n",
        type=separator,
    )
    parser.add_argument(
        '-n',
        '--rows',
        type=rows,
        default=sys.maxsize,
        help='number of rows to show',
    )
    parser.add_argument(
        '-j',
        '--justify',
        nargs='+',
        default=['<'],
        help='which justification to use\ndefault is left\nchoices: {l, r}\n'
            + 'can provide a list, in which case\none choice for each column',
        type=justification,
    )
    parser.add_argument(
        '-d',
        '--decorator',
        type=str,
        default=' ',
        help='which string/decorator to use in spacing',
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--header',
        action='store_true',
        help='header decoration',
    )
    group.add_argument(
        '--markdown',
        action='store_true',
        help='output markdown table',
    )
    return parser

def print_message_and_exit(parser, message):
    script_name = 'csvprint'
    parser.print_usage()
    print(f"{script_name}: error:", end=' ')
    print(message)
    sys.exit()

def file_error_checking(parser, args):
    reading_from_pipe = not sys.stdin.isatty() and args['filename'] == None
    if reading_from_pipe:
        args['csvfile'] = sys.stdin
    elif args['filename'] == None:
        print_message_and_exit(
            parser,
            "required: filename or pipe",
        )
    else:
        try:
            args['csvfile'] = open(args['filename'])
        except FileNotFoundError:
            print_message_and_exit(parser, f"no such file: {args['filename']}")

def markdown_options(parser, markdown, header, decorator):
    if markdown and header:
        print_message_and_exit(
            parser,
            "cannot use --header with --markdown"
        )
    if markdown and decorator is not ' ':
        print_message_and_exit(
            parser,
            "cannot use decorator with --markdown"
        )

def check_errors(parser, args):
    file_error_checking(parser, args)
    return args

def parse_cli_arguments(parser):
    args = vars(parser.parse_args())
    args = check_errors(parser, args)
    if args['markdown']:
        args['decorator'] = ' | '
    return args

def store_content(parser, args):
    csvreader = csv.reader(args['csvfile'], delimiter=args['separator'])
    header = next(csvreader)
    args['widths'] = [len(cell) for cell in list(header)]
    args['num_columns'] = len(args['widths'])
    justify_all_columns_equally = len(args['justify']) == 1
    justification_and_columns_differ = len(args['justify']) != args['num_columns']
    if justify_all_columns_equally:
        args['justify'] = [args['justify'][0]] * args['num_columns']
    elif justification_and_columns_differ:
        print_message_and_exit(
            parser,
            'argument -j/--justify: only one argument or one per column'
        )
    args['content'] = [header]
    row_number = 0
    for row_number, row in enumerate(islice(csvreader, args['rows'] - 1)):
        args['widths'], content = store_row(row_number, row, args)
        args['content'].append(content)
    args['rows'] = row_number + 1
    args['total_width'] = sum(args['widths']) + (args['num_columns']-1)*len(args['decorator'])

def store_row(row_number, row, args):
    row_content = []
    widths = []
    for cell_num, cell in enumerate(row):
        widths.append(max(len(cell), args['widths'][cell_num]))
        row_content.append(cell)
    return widths, row_content