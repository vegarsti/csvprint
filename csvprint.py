#!/usr/bin/env python3

import sys
import parser

def markdown_justification(direction):
    return {'>': ':', '<': '-'}[direction]

def header_line(length, border='-'):
    return f'{border*length}'

def row_output(justify, widths, decorator, row, row_number):
    cells = []
    for cell_num, cell in enumerate(row):
        cells.append('{:{align}{width}}'.format(
            cell,
            align=justify[cell_num],
            width=widths[cell_num],
        ))
    return decorator.join(cells)

def get_output(args):
    rows = []
    for row_number, row in enumerate(args['content']):
        is_first_row = row_number == 0
        normal_header = args['header'] and is_first_row
        markdown_header = args['markdown'] and is_first_row
        if normal_header:
            rows.append(header_line(args['total_width']))
        rows.append(row_output(
            args['justify'],
            args['widths'],
            args['decorator'],
            row,
            row_number,
        ))
        if normal_header:
            rows.append(header_line(args['total_width']))
        if markdown_header:
            rows.append(add_markdown_header(
                args['widths'],
                args['num_columns'],
                args['decorator'],
                args['justify'],
            ))
    return '\n'.join(rows)

def add_markdown_header(widths, num_columns, decorator, justify):
    cells = []
    for cell_num, width in enumerate(widths):
        first_or_last_column = cell_num == 0 or cell_num == num_columns - 1
        offset = 2
        if first_or_last_column:
            offset += 1
        total_cell_width = width + len(decorator) - offset
        suffix = markdown_justification(justify[cell_num])
        cells.append(f'{header_line(total_cell_width)}{suffix}')
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