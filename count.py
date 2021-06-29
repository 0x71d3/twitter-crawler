import argparse
import glob
import os
from collections import Counter

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('data_dir')
args = parser.parse_args()

c = Counter()

for tsv in glob.glob(f'{args.data_dir}/*.tsv'):
    n_turns = int(os.path.splitext(os.path.basename(tsv))[0])
    with open(tsv, encoding='utf-8') as f:
        n_dialogs = len(list(f))
        
        c[n_turns] = n_dialogs

print(c)

fig, ax = plt.subplots()
ax.bar(c.keys(), c.values())
plt.show()
