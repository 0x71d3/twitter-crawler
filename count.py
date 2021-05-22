import csv
import glob
from collections import Counter

from tqdm import tqdm
import matplotlib.pyplot as plt

print('cleaned.tsv')

c = Counter()

with open('cleaned.tsv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    for row in reader:
        c[len(row)] += 1

print(c)

# fig, ax = plt.subplots()
# ax.bar(c_len.keys(), c_len.values())
# plt.show()

print('\nsub/')

c_sub = Counter()

for tsv in glob.glob('sub/*.tsv'):
    with open(tsv, encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            c_sub[len(row)] += 1

print(c_sub)
