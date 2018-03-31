def normalize_columns(args):
    for row in args['content']:
        while len(row) < args['num_columns']:
            row.append('')

def get_column_widths(args):
    return [max(map(len, col)) for col in zip(*args['content'])]

def pad_cells(args):
    column_widths = get_column_widths(args)
    for row in args['content']:
        num_cells = len(row)
        for cell_num, cell in enumerate(row):
            row[cell_num] = '{:{align}{width}}'.format(
                cell,
                align=args['justify'][cell_num],
                width=column_widths[cell_num],
            )

def header_line(length, border='-'):
    return f'{border*length}'

def md_justification(justification):
    if justification == '<':
        return ':', '-'
    elif justification == '>':
        return '-', ':'
    else:
        return '-', '-'

def markdown_header(args):
    widths = get_column_widths(args)
    content = []
    for i, w in enumerate(widths):
        if w < 3:
            raise ValueError
        left, right = md_justification(args['justify'][i])
        content.append(left + '-'*(w-2) + right)
    return content

def add_header(args):
    widths = get_column_widths(args)
    if args['markdown']:
        args['content'].insert(
            1,
            markdown_header(args),
        )
    if args['header']:
        for index in (0, 2):
            args['content'].insert(
                index,
                '-'*sum(widths),
            )

def add_padding(args):
    for i, row in enumerate(args['content']):
        padding_string = ' '*args['padding']
        for j, cell in enumerate(row):
            left = padding_string
            right = padding_string
            if j == 0:
                left = ''
            elif j == len(row) - 1:
                right = ''
            args['content'][i][j] = left + args['content'][i][j] + right

def add_divider(args):
    for i, row in enumerate(args['content']):
        args['content'][i] = args['decorator'].join(args['content'][i])

def run_pipeline(args):
    normalize_columns(args)
    pad_cells(args)
    add_padding(args)
    add_header(args)
    add_divider(args)
    return '\n'.join(args['content'])