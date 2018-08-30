def copy_nested_list(l):
    """Return a copy of list l to one level of nesting"""
    return [list(i) for i in l]


def normalize_table(table, n):
    """Return a normalized version of table such that it has n columns in each row, possibly with empty cells"""
    normalized_table = copy_nested_list(table)
    for row in normalized_table:
        while len(row) < n:
            row.append("")
    return normalized_table


def column_widths(table):
    """Get the maximum size for each column in table"""
    return [max(map(len, col)) for col in zip(*table)]


def align_table(table, align):
    """Return table justified according to align"""
    widths = column_widths(table)
    new_table = copy_nested_list(table)
    for row in new_table:
        for cell_num, cell in enumerate(row):
            row[cell_num] = "{:{align}{width}}".format(
                cell, align=align[cell_num], width=widths[cell_num]
            )
    return new_table


def header_line(length, border="-"):
    """Return header of length"""
    return border * length


def md_alignment(alignment):
    """Given alignment option, return corresponding markdown"""
    if alignment == "<":
        return ":", "-"
    elif alignment == ">":
        return "-", ":"
    else:
        return "-", "-"


def latex_alignment(alignment):
    """Given alignment option, return corresponding latex"""
    if alignment == "<":
        return "l"
    elif alignment == ">":
        return "r"


def markdown_header(table, align):
    """Get markdown header for table according to given alignment options"""
    widths = column_widths(table)
    header_line = []
    for i, w in enumerate(widths):
        if w < 3:
            raise ValueError
        left, right = md_alignment(align[i])
        header_line.append(left + "-" * (w - 2) + right)
    return header_line


def add_markdown_header(table, align):
    """Add markdown header lines to table"""
    new_table = copy_nested_list(table)
    new_table.insert(1, markdown_header(table, align))
    return new_table


def add_header(table, align):
    """Add header lines to table"""
    widths = column_widths(table)
    new_table = copy_nested_list(table)
    for index in (0, 2):
        new_table.insert(index, [header_line(w) for w in widths])
    return new_table


def add_padding(table, padding):
    """Return a version of table which is padded according to inputted padding"""
    new_table = copy_nested_list(table)
    for i, row in enumerate(new_table):
        padding_string = " " * padding
        for j, cell in enumerate(row):
            left = padding_string
            right = padding_string
            if j == 0:
                left = ""
            elif j == len(row) - 1:
                right = ""
            new_table[i][j] = left + new_table[i][j] + right
    return new_table


def join_columns_with_divider(table, decorator):
    """Join each line in table with the decorator string between each cell"""
    return [decorator.join(row) for row in table]


def join_formatted_lines(lines):
    """Return the finished output"""
    return "\n".join(lines)


def add_latex_line_endings(lines):
    """Add latex newline character to each line"""
    return [line + r" \\" for line in lines]


def add_latex_table_environment(lines, number_of_columns, alignment):
    """Add latex environment specification"""
    lines = list(lines)
    latex_alignments = [latex_alignment(j) for j in alignment]
    alignment_line = "{{{}}}".format("".join(latex_alignments))
    lines.insert(0, r"\begin{tabular}" + alignment_line)
    lines.append(r"\end{tabular}")
    return lines


def right_strip_lines(lines):
    """Remove trailing spaces on each line"""
    return [line.rstrip() for line in lines]


def select_columns_from_table(table, columns, alignment):
    new_table = []
    new_alignment = []
    for row in table:
        new_row = []
        for column_number in columns:
            index_number = column_number - 1
            cell = row[index_number]
            new_row.append(cell)
        new_table.append(new_row)
    for column_number in columns:
        index_number = column_number - 1
        new_alignment.append(alignment[index_number])
    return new_table, new_alignment


def run_pipeline(args):
    """Run the printing pipeline according to arguments given"""
    raw_table = args["content"]
    alignment = args["align"]
    padding = args["padding"]
    output_as_markdown = args["markdown"]
    output_as_latex = args["latex"]
    output_as_header = args["header"]
    decorator = args["decorator"]
    columns_to_print = args["columns"]
    number_of_columns = len(columns_to_print)
    raw_table_subset, alignment_subset = select_columns_from_table(
        raw_table, columns_to_print, alignment
    )
    normalized_table = normalize_table(raw_table_subset, number_of_columns)
    justified_table = align_table(normalized_table, alignment_subset)
    padded_table = add_padding(justified_table, padding)
    if output_as_markdown:
        padded_table = add_markdown_header(padded_table, alignment_subset)
    if output_as_header:
        padded_table = add_header(padded_table, alignment_subset)
    lines = join_columns_with_divider(padded_table, decorator)
    if output_as_latex:
        lines = add_latex_line_endings(lines)
        lines = add_latex_table_environment(lines, number_of_columns, alignment)
    else:
        lines = right_strip_lines(lines)
    finished_output = join_formatted_lines(lines)
    return finished_output
