import csv
from collections import Counter

c_len = Counter()

with open('cleaned.tsv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    for row in reader:
        c_len[len(row)] += 1

print(c_len)
