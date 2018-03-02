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
    if direction == 'r':
        right_character = ':'
    else:
        right_character = '-'
    return '-', right_character

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
        help='which justification to use\ndefault is left\nchoices: {l, r}\ncan provide a list, in which case one \nchoice for each column',
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

def check_errors(parser, args):
    if args['rows'] <= 0:
        print_message_and_exit(
            parser,
            "argument -n/--rows must be a positive integer",
        )
    if not sys.stdin.isatty() and args['filename'] == None:
        args['csvfile'] = sys.stdin
    elif args['filename'] == None:
        print_message_and_exit(
            parser,
            "the following arguments are required: filename",
        )
    else:
        try:
            args['csvfile'] = open(args['filename'], 'r')
        except FileNotFoundError:
            print_message_and_exit(
                parser,
                f"no such file: {args['filename']}",
            )

def parse_cli_arguments(parser):
    args = vars(parser.parse_args())
    if args['markdown']:
        args['decorator'] = ' | '
        args['md_prefix'], args['md_suffix'] = markdown_justification(
            justification[i]
        )
    check_errors(parser, args)
    return args

def store_content(args):
    csvfile = args['csvfile']
    max_rows = args['rows']
    separator = args['separator']
    csvreader = csv.reader(csvfile, delimiter=separator)
    header = next(csvreader)
    widths = [len(cell) for cell in list(header)]
    args['number_of_columns'] = len(widths)
    number_of_columns = args['number_of_columns']
    args['content'] = [header]
    for row_number, row in enumerate(islice(csvreader, max_rows - 1)):
        row_content = []
        number_of_cells = len(row)
        if number_of_cells != number_of_columns:
            print_message_and_exit(
                parser,
                "not a properly formatted csv file, or "
                +"'{separator}' is an incorrect separator character".format(separator=separator),
            )
        for i, cell in enumerate(row):
            widths[i] = max(len(cell), widths[i])
            row_content.append(cell)
        args['content'].append(row_content)
    args['rows'] = row_number + 1
    args['widths'] = [l for l in widths]
    widths, decorator = args['widths'], args['decorator']
    args['total_width'] = sum(widths) + (len(widths)-1)*len(decorator)

def get_output(args):
    content = args['content']
    widths = args['widths']
    justification = args['justify']
    decorator = args['decorator']
    header = args['header']
    markdown = args['markdown']
    total_width = args['total_width']
    number_of_columns = len(widths)
    if len(justification) == 1:
        justification = [justification[0]]*number_of_columns
    elif len(justification) != number_of_columns:
        print_message_and_exit('number of justification arguments not equal number of columns')
    try:
        py_justification = [justification_translator(j) for j in justification]
    except ValueError:
        print_message_and_exit(
            f"incorrect justification option: {justification[0]}\n" +
            "options: l/left for left and r/right for right"
        )
    total_output = ''
    for row_number, row in enumerate(content):
        output = ''
        if header and row_number == 0:
            output += '-'*total_width + '\n'
        number_of_cells = len(row)
        for i in range(number_of_columns):
            output += ('{:' + py_justification[i] + '{width}}').format(row[i],
                width=widths[i])
            if i < len(widths) - 1:
                output += decorator
        if header and row_number == 0:
            output += '\n' + '-'*(total_width)
        if markdown and row_number == 0:
            output += add_markdown_styling(args)
        total_output += output
        if row_number < args['rows']:
            total_output += '\n'
    if not args['csvfile'] == sys.stdin:
        args['csvfile'].close()
    return total_output

def add_markdown_styling(args):
    justification = args['justify']
    number_of_columns = args['number_of_columns']
    decorator = args['decorator']
    output = '\n'
    for i, l in enumerate(args['widths']):
        md_prefix, md_suffix = args['md_prefix'], args['md_suffix']
        offset = 3
        if i == 0 or i == number_of_columns - 1:
            offset = 4
        output += md_prefix + '-'*(l+len(decorator)-offset) + md_suffix
        if i < number_of_columns - 1:
            output += '|'
    return output

def main():
    parser = create_parser()
    args = parse_cli_arguments(parser)
    store_content(args)
    output = get_output(args)
    print(output)

if __name__ == '__main__':
    main()