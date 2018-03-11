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
    use_tab_separator = args['separator'] == r'\t'
    if use_tab_separator:
        args['separator'] = '\t'
    csvreader = csv.reader(args['csvfile'], delimiter=args['separator'])
    header = next(csvreader)
    args['widths'] = [len(cell) for cell in list(header)]
    args['number_of_columns'] = len(args['widths'])
    number_of_columns = args['number_of_columns']
    justify_all_columns_equally = len(args['justify']) == 1
    number_of_columns_differ_from_justification = len(args['justify']) != number_of_columns
    if justify_all_columns_equally:
        args['justify'] = [args['justify'][0]] * number_of_columns
    elif number_of_columns_differ_from_justification:
        print_message_and_exit(
            parser,
            'number of justification arguments not equal number of columns'
        )
    args['content'] = [header]
    row_number = 0
    for row_number, row in enumerate(islice(csvreader, args['rows'] - 1)):
        args['widths'], content = store_row(row_number, row, args, parser)
        args['content'].append(content)
    args['rows'] = row_number + 1
    args['total_width'] = sum(args['widths']) + (args['number_of_columns']-1)*len(args['decorator'])

def store_row(row_number, row, args, parser):
    number_of_cells = len(row)
    if number_of_cells != args['number_of_columns'] or number_of_cells == 1:
        print_message_and_exit(
            parser,
            f"not a properly formatted csv file, or '{args['separator']}'\n"
                + 'is an incorrect separator character'
        )
    row_content = []
    widths = []
    for i, cell in enumerate(row):
        widths.append(max(len(cell), args['widths'][i]))
        row_content.append(cell)
    return widths, row_content

def header_line(length, border='-'):
    return f'{border*length}'

def row_output(args, row, row_number):
    cells = []
    for i in range(args['number_of_columns']):
        cells.append('{:{align}{width}}'.format(
            row[i],
            align=args['justify'][i],
            width=args['widths'][i],
        ))
    return args['decorator'].join(cells)

def get_output(args):
    rows = []
    for row_number, row in enumerate(args['content']):
        header = args['header'] and row_number == 0
        markdown = args['markdown'] and row_number == 0
        if header:
            rows.append(header_line(args['total_width']))
        rows.append(row_output(args, row, row_number))
        if header:
            rows.append(header_line(args['total_width']))
        if markdown:
            rows.append(add_markdown_header(args))
    return '\n'.join(rows)

def add_markdown_header(args):
    cells = []
    for i, l in enumerate(args['widths']):
        prefix, suffix = markdown_justification(args['justify'][i])
        first_or_last_column = i == 0 or i == args['number_of_columns'] - 1
        offset = 3
        if first_or_last_column:
            offset += 1
        column_length = l+len(args['decorator'])-offset
        border = '-'
        cells.append(f'{prefix}{header_line(column_length)}{suffix}')
    return '|'.join(cells)

def main():
    parser = create_parser()
    args = parse_cli_arguments(parser)
    store_content(parser, args)
    output = get_output(args)
    reading_from_csvfile = not args['csvfile'] == sys.stdin
    if reading_from_csvfile:
        args['csvfile'].close()
    print(output)

if __name__ == '__main__':
    main()