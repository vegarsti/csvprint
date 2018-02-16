#! /usr/bin/env python3

import argparse
import csv
import sys
from itertools import islice

def justification_translator(direction):
    if direction == 'left' or direction == 'l':
        return '<'
    elif direction == 'right' or direction == 'r':
        return '>'
    else:
        raise ValueError

def markdown_justification(direction, suffix=False):
    if direction == 'right' or direction == 'r':
        left, right = '-', ':'
    else:
        left, right = '-', '-'
    return left, right

script_name = 'csvprint'

parser = argparse.ArgumentParser(
    description='Command line utility for pretty printing csv files.',
    formatter_class=argparse.RawTextHelpFormatter,
    prog=script_name
)

def print_message_and_exit(message):
    parser.print_usage()
    print(f"{script_name}: error:", end=' ')
    print(message)
    sys.exit()

def parse_cli_arguments(use_stdin_as_file=False):
    parser.add_argument('filename', type=str, help='file to pretty print', nargs='?')

    parser.add_argument('-s', '--separator', type=str, default=',',
        help='separator/delimiter used in csv file\ndefault is comma')
    parser.add_argument('-n', '--rows', type=int, default=sys.maxsize,
        help='number of rows to show')
    parser.add_argument('-j', '--justify', nargs='+',
        default=['left'],
        help='which justification to use\ndefault is left\nchoices: {left, right}\ncan provide a list, in which case one \nchoice for each column')
    parser.add_argument('-d', '--decorator', type=str,
        default=' ', help='which string/decorator to use in spacing')
    parser.add_argument('--header', action='store_true',
        help='header decoration')
    parser.add_argument('--markdown', action='store_true',
        help='output valid markdown table')
    args = vars(parser.parse_args())
    if args['markdown']:
        args['decorator'] = ' | '
    return args

def read_content(csvfile, max_rows, separator):        
    csvreader = csv.reader(csvfile, delimiter=separator)
    header = next(csvreader)
    lengths = [len(cell) for cell in list(header)]
    number_of_columns = len(lengths)
    content = [header]
    for row_number, row in enumerate(islice(csvreader, max_rows)):
        row_content = []
        number_of_cells = len(row)
        if number_of_cells != number_of_columns:
            print_message_and_exit("not a properly formatted csv file, or "
                +"'{separator}' is an incorrect separator character".format(
                separator=separator)
            )
        for i, cell in enumerate(row):
            lengths[i] = max(len(cell), lengths[i])
            row_content.append(cell)
        content.append(row_content)
    lengths = [l for l in lengths]
    return content, lengths

def get_output(content, lengths, justification, decorator, header, markdown):
    total_length = sum(lengths) + (len(lengths)-1)*len(decorator)
    number_of_columns = len(lengths)
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
            output += '-'*total_length + '\n'
        number_of_cells = len(row)
        for i in range(number_of_columns):
            output += ('{:' + py_justification[i] + '{width}}').format(row[i],
                width=lengths[i])
            if i < len(lengths) - 1:
                output += decorator
        if header and row_number == 0:
            output += '\n' + '-'*(total_length)
        if markdown and row_number == 0:
            output += add_markdown_styling(
                row_number, lengths, justification,
                number_of_columns, decorator
            )
        total_output += output + '\n'
    return total_output

def add_markdown_styling(row_number, lengths, justification, number_of_columns, decorator):
    output = '\n'
    for i, l in enumerate(lengths):
        md_prefix, md_suffix = markdown_justification(justification[i])
        offset = 3
        if i == 0 or i == number_of_columns - 1:
            offset = 4
        output += md_prefix + '-'*(l+len(decorator)-offset) + md_suffix
        if i < number_of_columns - 1:
            output += '|'
    return output


def main():
    args = parse_cli_arguments()

    if args['rows'] <= 0:
        print_message_and_exit("argument -n/--rows must be a positive integer")

    if not sys.stdin.isatty() and args['filename'] == None:
        csvfile = sys.stdin
    elif args['filename'] == None:
        print_message_and_exit("the following arguments are required: filename")
    else:
        try:
            csvfile = open(args['filename'], 'r')
        except FileNotFoundError:
            print_message_and_exit(f"no such file: {filename}")

    content, lengths = read_content(
        csvfile=csvfile,
        max_rows=args['rows'],
        separator=args['separator']
    )
    if not csvfile == sys.stdin:
        csvfile.close()
    output = get_output(
        content, lengths, args['justify'], args['decorator'],
        header=args['header'], markdown=args['markdown']
    )
    print(output)

if __name__ == '__main__':
    main()