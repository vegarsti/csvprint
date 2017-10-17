import csv

from sys import exit

import argparse
from argparse import RawTextHelpFormatter

def setup_argparse():
    parser = argparse.ArgumentParser(
        description='Command line utility for pretty printing csv files.',
        formatter_class=RawTextHelpFormatter,
        prog='pycolumn'
    )
    parser.add_argument('filename', type=str, help='file to pretty print')
    parser.add_argument('-s', '--separator', type=str, default=',',
        help='separator/delimiter used in the csv file\ndefault is ,')
    parser.add_argument('-w', '--width', type=int, default=1,
        help='width of space between columns\ndefault is 1')
    parser.add_argument('-r', '--rows', type=int, default=1000,
        help='number of rows to show\ndefault is 1000')
    args = parser.parse_args()
    return args

def read_content(filename, max_rows, separator, spacing):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=separator)
        header = next(csvreader)
        lengths = [len(i) for i in list(header)]
        content = [header]
        for num_rows, row in enumerate(csvreader):
            row_content = []
            if num_rows < max_rows - 1:
                for i, cell in enumerate(row):
                    lengths[i] = max(len(cell), lengths[i])
                    row_content.append(cell)
                content.append(row_content)
    lengths = [l + spacing for l in lengths]
    return content, lengths

def print_output(content, lengths):
    for row in content:
        output = ''
        for i in range(len(lengths)):
            output += '{0:>{width}}'.format(row[i], width=lengths[i])
        print(output)

def main():
    args = setup_argparse()
    content, lengths = read_content(
        filename=args.filename,
        max_rows=args.rows,
        separator=args.separator,
        spacing=args.width
    )
    print_output(content, lengths)

if __name__ == '__main__':
    main()