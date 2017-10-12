import csv

from sys import exit

import argparse

def print_usage_and_exit(parser, string=None):
    if string: print(string)
    parser.print_usage()
    exit()

def main():
    # Set up argparse
    parser = argparse.ArgumentParser(
        description='Command line utility for pretty printing csv files'
    )
    parser.add_argument('-f', '--filename', type=str, nargs=1,
        help='filename')
    parser.add_argument('-d', '--delimiter', type=str, nargs=1,
        help='delimiter', default=',')
    args = parser.parse_args()

    if not args.filename:
        print_usage_and_exit(parser)

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=delimiter)
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