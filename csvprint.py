#! /usr/bin/env python3

import argparse
import csv
import sys
from itertools import islice

def justification_translator(direction):
    if direction == 'l':
        return '<'
    elif direction == 'r':
        return '>'
    else:
        raise ValueError

def markdown_justification(direction):
    return '-', {'>': ':', '<': '-'}[direction]

def print_message_and_exit(parser, message):
    script_name = 'csvprint'
    parser.print_usage()
    print(f"{script_name}: error:", end=' ')
    print(message)
    sys.exit()

def create_parser():
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
        help='separator/delimiter used in csv file\ndefault is comma',
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
        help='which justification to use\ndefault is left\nchoices: {l, r}\n' +
            'can provide a list, in which case one \nchoice for each column',
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
        help='output valid markdown table',
    )
    return parser

def file_error_checking(parser, args):
    if not sys.stdin.isatty() and args['filename'] == None:
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
            print_message_and_exit(
                parser,
                f"no such file: {args['filename']}",
            )

def justification_error_checking(parser, args):
    try:
        args['justify'] = [justification_translator(j) for j in args['justify']]
    except ValueError:
        print_message_and_exit(
            parser,
            f"incorrect justification option: {args['justify'][0]}\n" +
            "options: l/left for left and r/right for right"
        )

def number_of_rows_error_checking(parser, args):
    if args['rows'] <= 0:
            print_message_and_exit(
                parser,
                "argument -n/--rows must be a positive integer",
            )

def check_errors(parser, args):
    number_of_rows_error_checking(parser, args)
    file_error_checking(parser, args)
    justification_error_checking(parser, args)
    return args

def parse_cli_arguments(parser):
    args = vars(parser.parse_args())
    args = check_errors(parser, args)
    return args

def store_content(parser, args):
    if args['markdown']:
        args['decorator'] = ' | '
    csvreader = csv.reader(args['csvfile'], delimiter=args['separator'])
    header = next(csvreader)
    args['widths'] = [len(cell) for cell in list(header)]
    args['number_of_columns'] = len(args['widths'])
    number_of_columns = args['number_of_columns']
    if len(args['justify']) == 1:
        args['justify'] = [args['justify'][0]] * number_of_columns
    elif len(args['justify']) != number_of_columns:
        print_message_and_exit(
            parser,
            'number of justification arguments not equal number of columns'
        )
    args['content'] = [header]
    row_number = 0
    for row_number, row in enumerate(islice(csvreader, args['rows'] - 1)):
        args['widths'], content = store_row(row_number, row, args)
        args['content'].append(content)
    args['rows'] = row_number + 1
    args['total_width'] = sum(args['widths']) + (args['number_of_columns']-1)*len(args['decorator'])


def store_row(row_number, row, args):
    number_of_cells = len(row)
    if number_of_cells != args['number_of_columns'] or number_of_cells == 1:
        print_message_and_exit(
            parser,
            f'not a properly formatted csv file, or {separator}\n' +
            'is an incorrect separator character'
        )
    row_content = []
    widths = []
    for i, cell in enumerate(row):
        widths.append(max(len(cell), args['widths'][i]))
        row_content.append(cell)
    return widths, row_content


def header_line(border, length):
    return f'{border*length}'

def row_output(args, row, row_number):
    cells = []
    border = '-'
    for i in range(args['number_of_columns']):
        cells.append('{:{align}{width}}'.format(
            row[i],
            align=args['justify'][i],
            width=args['widths'][i],
        ))
    return args['decorator'].join(cells)

def get_output(args):
    border = '-'
    rows = []
    for row_number, row in enumerate(args['content']):
        if args['header'] and row_number == 0:
            rows.append(header_line(border, args['total_width']))
        rows.append(row_output(args, row, row_number))
        if args['header'] and row_number == 0:
            rows.append(header_line(border, args['total_width']))
        if args['markdown'] and row_number == 0:
            rows.append(add_markdown_header(args))
    return '\n'.join(rows)

def add_markdown_header(args):
    justification = args['justify']
    cells = []
    for i, l in enumerate(args['widths']):
        md_prefix, md_suffix = markdown_justification(args['justify'][i])
        offset = 3
        if i == 0 or i == args['number_of_columns'] - 1:
            offset += 1
        column_length = l+len(args['decorator'])-offset
        border = '-'
        cells.append(f'{md_prefix}{header_line(border, column_length)}{md_suffix}')
    return '|'.join(cells)

def main():
    parser = create_parser()
    args = parse_cli_arguments(parser)
    store_content(parser, args)
    output = get_output(args)
    if not args['csvfile'] == sys.stdin:
        args['csvfile'].close()
    print(output)

if __name__ == '__main__':
    main()