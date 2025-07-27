import csv

with inplace(csvfilename, 'r', newline='') as (infile, outfile):
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for row in reader:
        row += ['new', 'columns']
        writer.writerow(row)