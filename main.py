import csv
filename = 'box-prediction/products_per_supplier.csv'
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    header = next(csvreader)
    lengths = [0]*len(list(header))
    for row in csvreader:
        for i, cell in enumerate(row):
            lengths[i] = max(len(cell), lengths[i])
    lengths = [l + 1 for l in lengths]
    print(lengths)
    s = ""
    for i, l in enumerate(lengths):
        s += "{}"
        row = "%s"*len(lengths)