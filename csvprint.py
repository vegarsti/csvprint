#! /usr/bin/env python3

import sys
import parser

def markdown_justification(direction):
    return '-', {'>': ':', '<': '-'}[direction]

def header_line(length, border='-'):
    return f'{border*length}'

def row_output(args, row, row_number):
    cells = []
    for cell_num, cell in enumerate(row):
        cells.append('{:{align}{width}}'.format(
            cell,
            align=args['justify'][cell_num],
            width=args['widths'][cell_num],
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
    for cell_num, width in enumerate(args['widths']):
        first_or_last_column = cell_num == 0 or cell_num == args['num_columns'] - 1
        offset = 3
        if first_or_last_column:
            offset += 1
        column_length = width + len(args['decorator']) - offset
        prefix, suffix = markdown_justification(args['justify'][cell_num])
        cells.append(f'{prefix}{header_line(column_length)}{suffix}')
    return '|'.join(cells)

def main():
    csvparser = parser.create()
    args = parser.parse_cli_arguments(csvparser)
    parser.store_content(csvparser, args)
    output = get_output(args)
    reading_from_csvfile = not args['csvfile'] == sys.stdin
    if reading_from_csvfile:
        args['csvfile'].close()
    print(output)

if __name__ == '__main__':
    main()