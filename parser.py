import argparse
import sys
import csv
from itertools import islice

def justification_translator(direction):
    if direction == 'l':
        return '<'
    elif direction == 'r':
        return '>'
    else:
        raise ValueError

def create():
    script_name = 'csvprint'
    parser = argparse.ArgumentParser(
        description='Command line utility for pretty printing csv files.',
        formatter_class=argparse.RawTextHelpFormatter,
        prog=script_name
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
        type=str,
        default=',',
        help='separator/delimiter used in csv file\ndefault is comma\nuse \\t for tabs',
    )
    parser.add_argument(
        '-n',
        '--rows',
        type=int,
        default=sys.maxsize,
        help='number of rows to show',
    )
    parser.add_argument(
        '-j',
        '--justify',
        nargs='+',
        default=['l'],
        help='which justification to use\ndefault is left\nchoices: {l, r}\n'
            + 'can provide a list, in which case\none choice for each column',
    )
    parser.add_argument(
        '-d',
        '--decorator',
        type=str,
        default=' ',
        help='which string/decorator to use in spacing',
    )
    parser.add_argument(
        '--header',
        action='store_true',
        help='header decoration'
    )
    parser.add_argument(
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
            "the following arguments are required: filename",
        )
    else:
        try:
            args['csvfile'] = open(args['filename'])
        except FileNotFoundError:
            print_message_and_exit(parser, f"no such file: {args['filename']}")

def justification_error_checking(parser, args):
    try:
        args['justify'] = [justification_translator(j) for j in args['justify']]
    except ValueError:
        print_message_and_exit(
            parser,
            f"argument -j/--justify: invalid justification option: '{args['justify'][0]}'\n" +
            "options: l/left for left and r/right for right"
        )

def number_of_rows_error_checking(parser, args):
    if args['rows'] <= 0:
            print_message_and_exit(
                parser,
                "argument -n/--rows: expected positive integer",
            )

def only_markdown_or_header(parser, args):
    if args['markdown'] and args['header']:
        print_message_and_exit(
            parser,
            "cannot use --header with --markdown"
        )

def check_errors(parser, args):
    number_of_rows_error_checking(parser, args)
    file_error_checking(parser, args)
    justification_error_checking(parser, args)
    only_markdown_or_header(parser, args)
    return args

def parse_cli_arguments(parser):
    args = vars(parser.parse_args())
    args = check_errors(parser, args)
    if args['markdown']:
        args['decorator'] = ' | '
    using_tab_separator = args['separator'] == r'\t'
    if using_tab_separator:
        args['separator'] = '\t'
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
        args['widths'], content = store_row(row_number, row, args, parser)
        args['content'].append(content)
    args['rows'] = row_number + 1
    args['total_width'] = sum(args['widths']) + (args['num_columns']-1)*len(args['decorator'])

def store_row(row_number, row, args, parser):
    mismatching_row_length = len(row) != args['num_columns'] or len(row) == 1
    if mismatching_row_length:
        print_message_and_exit(
            parser,
            f"not a properly formatted csv file, or '{args['separator']}'\n"
                + 'is an incorrect separator character'
        )
    row_content = []
    widths = []
    for cell_num, cell in enumerate(row):
        widths.append(max(len(cell), args['widths'][cell_num]))
        row_content.append(cell)
    return widths, row_content