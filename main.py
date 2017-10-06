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
    lengths = [0]*len(list(header))
    content = []
    for row in csvreader:
        row_content = []
        for i, cell in enumerate(row):
            lengths[i] = max(len(cell), lengths[i])
            row_content.append(cell)
        content.append(row_content)

lengths = [l + 1 for l in lengths]
row_length = len(lengths)
output_string = ''

for row in content:
    for i in range(row_length):
        output_string += '{0:>{width}}'.format(row[i], width=lengths[i])
    output_string += '\n'

# Remove last newline
output_string = output_string.strip()

print(output_string.strip())