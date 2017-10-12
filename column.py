import csv

from sys import exit

import argparse
from argparse import RawTextHelpFormatter

def print_usage_and_exit(parser, string=None):
    if string: print(string)
    parser.print_usage()
    exit()

def main():
    # Set up argparse
    parser = argparse.ArgumentParser(
        description='Command line utility for pretty printing csv files.',
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('filename', type=str, help='file to pretty print')
    parser.add_argument('-s', '--separator', type=str, default=',',
        help='separator/delimiter used in the csv file\ndefault is ,')
    args = parser.parse_args()

    filename = args.filename

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=args.separator)
        header = next(csvreader)
        lengths = [len(i) for i in list(header)]
        content = [header]
        for row in csvreader:
            row_content = []
            for i, cell in enumerate(row):
                lengths[i] = max(len(cell), lengths[i])
                row_content.append(cell)
            content.append(row_content)

    lengths = [l + 1 for l in lengths]
    num_rows = len(lengths)

    for row in content:
        output = ''
        for i in range(num_rows):
            output += '{0:>{width}}'.format(row[i], width=lengths[i])
        print(output)

if __name__ == '__main__':
    main()