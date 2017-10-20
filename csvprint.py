import csv

from sys import exit

import argparse
from argparse import RawTextHelpFormatter

justification_translator = {
    'l': '<',
    'r': '>'
}

def parse_cli_arguments():
    parser = argparse.ArgumentParser(
        description='Command line utility for pretty printing csv files.',
        formatter_class=RawTextHelpFormatter,
        prog='csvprint'
    )
    parser.add_argument('filename', type=str, help='file to pretty print')
    parser.add_argument('-s', '--separator', type=str, default=',',
        help='separator/delimiter used in the csv file\ndefault is ,')
    parser.add_argument('-r', '--rows', type=int, default=1000,
        help='number of rows to show\ndefault is 1000')
    parser.add_argument('-j', '--justify', type=str, choices=('l', 'r'),
        default='r', help='which justification to use \ndefault is r (right)')
    parser.add_argument('-d', '--decorator', type=str,
        default=' ', help='which string/decorator to use in spacing')
    parser.add_argument('--header', action='store_true',
        help='turn on header decoration')
    args = parser.parse_args()
    args.justify = justification_translator[args.justify]
    return args

def read_content(filename, max_rows, separator):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=separator)
        header = next(csvreader)
        lengths = [len(cell) for cell in list(header)]
        content = [header]
        for row_number, row in enumerate(csvreader):
            row_content = []
            if row_number < max_rows - 1:
                for i, cell in enumerate(row):
                    lengths[i] = max(len(cell), lengths[i])
                    row_content.append(cell)
                content.append(row_content)
    lengths = [l for l in lengths]
    return content, lengths

def print_output(content, lengths, justification, decorator, header):
    total_length = sum(lengths) + (len(lengths)-1)*len(decorator)
    for row_number, row in enumerate(content):
        output = ''
        if header and row_number == 0:
            output += '-'*total_length + '\n'
        for i in range(len(lengths)):
            if i == 0:
                justification_now = justification_translator['l']
            else:
                justification_now = justification
            output += ('{:' + justification_now + '{width}}').format(row[i], width=lengths[i])
            if i < len(lengths) - 1:
                output += decorator
        if header and row_number == 0:
            output += '\n' + '-'*total_length
        print(output)

def main():
    args = parse_cli_arguments()
    content, lengths = read_content(
        filename=args.filename,
        max_rows=args.rows,
        separator=args.separator
    )
    print_output(content, lengths, args.justify, args.decorator, header=args.header)

if __name__ == '__main__':
    main()