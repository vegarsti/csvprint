def copy_nested_list(l):
    """Return a copy of list l to one level of nesting"""
    return [list(i) for i in l]

def normalize_table(table, n):
    """Return a normalized version of table such that it has n columns in each row, possibly with empty cells"""
    normalized_table = copy_nested_list(table)
    for row in normalized_table:
        while len(row) < n:
            row.append('')
    return normalized_table

def column_widths(table):
    """Get the maximum size for each column in table"""
    return [max(map(len, col)) for col in zip(*table)]

def justify_table(table, justify):
    """Return table justified according to justify"""
    widths = column_widths(table)
    new_table = copy_nested_list(table)
    for row in new_table:
        num_cells = len(row)
        for cell_num, cell in enumerate(row):
            row[cell_num] = '{:{align}{width}}'.format(
                cell,
                align=justify[cell_num],
                width=widths[cell_num],
            )
    return new_table

def header_line(length, border='-'):
    """Return header of length"""
    return border*length

def md_justification(justification):
    """Given justification option, return corresponding markdown"""
    if justification == '<':
        return ':', '-'
    elif justification == '>':
        return '-', ':'
    else:
        return '-', '-'

def latex_justification(justification):
    """Given justification option, return corresponding latex"""
    if justification == '<':
        return 'l'
    elif justification == '>':
        return 'r'

def markdown_header(table, justify):
    """Get markdown header for table according to given justification options"""
    widths = column_widths(table)
    header_line = []
    for i, w in enumerate(widths):
        if w < 3:
            raise ValueError
        left, right = md_justification(justify[i])
        header_line.append(left + '-'*(w-2) + right)
    return header_line

def add_markdown_header(table, justify):
    """Add markdown header lines to table"""
    widths = column_widths(table)
    new_table = copy_nested_list(table)
    new_table.insert(
        1,
        markdown_header(table, justify),
    )
    return new_table

def add_header(table, justify):
    """Add header lines to table"""
    widths = column_widths(table)
    new_table = copy_nested_list(table)
    for index in (0, 2):
        new_table.insert(
            index,
            [header_line(w) for w in widths],
        )
    return new_table

def add_padding(table, padding):
    """Return a version of table which is padded according to inputted padding"""
    new_table = copy_nested_list(table)
    for i, row in enumerate(new_table):
        padding_string = ' '*padding
        for j, cell in enumerate(row):
            left = padding_string
            right = padding_string
            if j == 0:
                left = ''
            elif j == len(row) - 1:
                right = ''
            new_table[i][j] = left + new_table[i][j] + right
    return new_table

def join_columns_with_divider(table, decorator):
    """Join each line in table with the decorator string between each cell"""
    return [decorator.join(row) for row in table]

def join_formatted_lines(lines):
    """Return the finished output"""
    return '\n'.join(lines)

def add_latex_line_endings(lines):
    """Add latex newline character to each line"""
    return [line + r' \\' for line in lines]

def add_latex_table_environment(lines, number_of_columns, justification):
    """Add latex environment specification"""
    lines = list(lines)
    latex_justifications = [latex_justification(j) for j in justification]
    justification_line = '{{{}}}'.format(''.join(latex_justifications))
    lines.insert(0, r'\begin{tabular}' + justification_line)
    lines.append('\end{tabular}')
    return lines

def right_strip_lines(lines):
    """Remove trailing spaces on each line"""
    return [line.rstrip() for line in lines]

def run_pipeline(args):
    """Run the printing pipeline according to arguments given"""
    raw_table = args['content']
    number_of_columns = args['num_columns']
    justification = args['justify']
    padding = args['padding']
    output_as_markdown = args['markdown']
    output_as_latex = args['latex']
    output_as_header = args['header']
    decorator = args['decorator']
    normalized_table = normalize_table(raw_table, number_of_columns)
    justified_table = justify_table(normalized_table, justification)
    padded_table = add_padding(justified_table, padding)
    if output_as_markdown:
        padded_table = add_markdown_header(padded_table, justification)
    if output_as_header:
        padded_table = add_header(padded_table, justification)
    lines = join_columns_with_divider(padded_table, decorator)
    if output_as_latex:
        lines = add_latex_line_endings(lines)
        lines = add_latex_table_environment(lines, number_of_columns, justification)
    else:
        lines = right_strip_lines(lines)
    finished_output = join_formatted_lines(lines)
    return finished_output