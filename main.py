import csv
from sys import argv

filename = argv[1]

if len(argv) == 3:
    delimiter = argv[2]
else:
    delimiter = ','

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