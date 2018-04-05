def copy_nested_list(l):
    return [list(i) for i in l]

def normalize_columns(content, num_columns):
    new_content = copy_nested_list(content)
    for row in new_content:
        while len(row) < num_columns:
            row.append('')
    return new_content

def get_column_widths(content):
    return [max(map(len, col)) for col in zip(*content)]

def pad_cells(content, justify):
    column_widths = get_column_widths(content)
    new_content = copy_nested_list(content)
    for row in new_content:
        num_cells = len(row)
        for cell_num, cell in enumerate(row):
            row[cell_num] = '{:{align}{width}}'.format(
                cell,
                align=justify[cell_num],
                width=column_widths[cell_num],
            )
    return new_content

def header_line(length, border='-'):
    return border*length

def md_justification(justification):
    if justification == '<':
        return ':', '-'
    elif justification == '>':
        return '-', ':'
    else:
        return '-', '-'

def markdown_header(content, justify):
    widths = get_column_widths(content)
    content = []
    for i, w in enumerate(widths):
        if w < 3:
            raise ValueError
        left, right = md_justification(justify[i])
        content.append(left + '-'*(w-2) + right)
    return content

def add_header(content, markdown, header, justify):
    widths = get_column_widths(content)
    new_content = copy_nested_list(content)
    if markdown:
        new_content.insert(
            1,
            markdown_header(content, justify),
        )
    if header:
        for index in (0, 2):
            new_content.insert(
                index,
                ['-'*w for w in widths],
            )
    return new_content

def add_padding(content, padding):
    new_content = copy_nested_list(content)
    for i, row in enumerate(new_content):
        padding_string = ' '*padding
        for j, cell in enumerate(row):
            left = padding_string
            right = padding_string
            if j == 0:
                left = ''
            elif j == len(row) - 1:
                right = ''
            new_content[i][j] = left + new_content[i][j] + right
    return new_content

def add_divider(content, decorator):
    return [decorator.join(row).rstrip() for row in content]

def join_lines(content):
    return '\n'.join(content)

def run_pipeline(args):
    content = normalize_columns(args['content'], args['num_columns'])
    content = pad_cells(content, args['justify'])
    content = add_padding(content, args['padding'])
    content = add_header(
        content,
        args['markdown'],
        args['header'],
        args['justify']
    )
    content = add_divider(content, args['decorator'])
    output = join_lines(content)
    return output