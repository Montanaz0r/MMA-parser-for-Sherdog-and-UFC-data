# Python 3.7
# appendix to sherdog-parser.py
# Created by - Montanaz0r (https://github.com/Montanaz0r)
# Some of records scrapped from sherdog did have tricky event names, for instance there was ',' inside double quote,
# it messed with reading these lines properly in Pandas so i have decided to help myself with regular expressions.
# Code below will adjust problematic lines.

import csv
import re

new_csv = []
with open('sherdog.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        new_row = []
        if len(row) == 1:
            subbed = re.sub(r'(?!(([^"]*"){2})*[^"]*$),', '', row[0])
            subbed = subbed.replace('"', '')
            subbed = subbed.replace('-', '')
            after_split = subbed.split(',')
            new_csv.append(after_split)
        else:
            for word in row:
                subbed = re.sub(r'(?!(([^"]*"){2})*[^"]*$),', '', word)
                subbed = subbed.replace('"', '')
                subbed = subbed.replace('-', '')
                new_row.append(subbed)
            new_csv.append(new_row)

with open('sherdog-subbed.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';', skipinitialspace=True)
    for line in new_csv:
        writer.writerow(line)




