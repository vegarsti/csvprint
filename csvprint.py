import csv

from sys import exit

import argparse
from argparse import RawTextHelpFormatter

justification_translator = {
    'left': '<',
    'right': '>',
    'l': '<',
    'r': '>',
}

markdown_justification = {
    'left': {'left': '-', 'right': '-'},
    'right': {'left': '-', 'right': ':'},
}

script_name = 'csvprint'

parser = argparse.ArgumentParser(
    description='Command line utility for pretty printing csv files.',
    formatter_class=RawTextHelpFormatter,
    prog=script_name
)

def print_and_exit(message):
    parser.print_usage()
    print("%s: error:" % script_name, end=' ')
    print(message)
    exit()

def parse_cli_arguments():
    parser.add_argument('filename', type=str, help='file to pretty print')
    parser.add_argument('-s', '--separator', type=str, default=',',
        help='separator/delimiter used in csv file\ndefault is comma')
    parser.add_argument('-n', '--rows', type=int, default=1000,
        help='number of rows to show\ndefault is 1000')
    parser.add_argument('-j', '--justify', nargs='+',
        default=['left'],
        help='which justification to use\ndefault is left\nchoices: {left, right}\ncan provide a list, in which case one \nchoice for each column')
    parser.add_argument('-d', '--decorator', type=str,
        default=' ', help='which string/decorator to use in spacing')
    parser.add_argument('--header', action='store_true',
        help='header decoration')
    parser.add_argument('--markdown', action='store_true',
        help='output valid markdown table')
    args = parser.parse_args()
    if args.markdown:
        args.decorator = ' | '
    return args

def read_content(filename, max_rows, separator):
    try:
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=separator)
            header = next(csvreader)
            lengths = [len(cell) for cell in list(header)]
            number_of_columns = len(lengths)
            content = [header]
            for row_number, row in enumerate(csvreader):
                if row_number == max_rows - 1:
                    break
                row_content = []
                number_of_cells = len(row)
                if number_of_cells != number_of_columns:
                    print_and_exit("not a properly formatted csv file, or "
                        +"'{separator}' is an incorrect separator character".format(
                        separator=separator)
                    )
                    exit()
                for i, cell in enumerate(row):
                    lengths[i] = max(len(cell), lengths[i])
                    row_content.append(cell)
                content.append(row_content)
    except FileNotFoundError:
        print_and_exit("no such file: {filename}".format(
            filename=filename.split('/')[-1])
        )
    lengths = [l for l in lengths]
    return content, lengths

def print_output(content, lengths, justification, decorator, header, markdown):
    total_length = sum(lengths) + (len(lengths)-1)*len(decorator)
    number_of_columns = len(lengths)
    if len(justification) == 1:
        justification = [justification[0]]*number_of_columns
    else:
        if len(justification) != number_of_columns:
            print_and_exit('number of justification arguments not equal number of columns')
    original_justification = justification
    justification = [justification_translator[j] for j in justification]
    left = '-'
    right = '-'
    for row_number, row in enumerate(content):
        output = ''
        if header and row_number == 0:
            output += '-'*total_length + '\n'
        number_of_cells = len(row)
        for i in range(number_of_columns):
            output += ('{:' + justification[i] + '{width}}').format(row[i],
                width=lengths[i])
            if i < len(lengths) - 1:
                output += decorator
        if header and row_number == 0:
            output += '\n' + left + '-'*(total_length-1) + right
        if markdown and row_number == 0:
            output += '\n'
            for i, l in enumerate(lengths):
                current = original_justification[i]
                md = markdown_justification[current]
                left = md['left']
                right = md['right']
                if i == 0 or i == number_of_columns - 1:
                    output += left + '-'*(l+len(decorator)-4) + right
                else:
                    output += left + '-'*(l + len(decorator)-3) + right
                if i < number_of_columns - 1:
                    output += '|'
        print(output)

def main():
    args = parse_cli_arguments()
    content, lengths = read_content(
        filename=args.filename,
        max_rows=args.rows,
        separator=args.separator
    )
    print_output(content, lengths, args.justify, args.decorator, header=args.header,
        markdown=args.markdown)

if __name__ == '__main__':
    main()