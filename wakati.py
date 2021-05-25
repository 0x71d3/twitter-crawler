import csv
import os

from tqdm import tqdm
import zenhan
from pyknp import Juman

jumanpp = Juman()

turn_dir = 'turn'
wakati_dir = 'wakati'

tsvs = sorted(os.listdir(turn_dir))

for tsv in tqdm(tsvs):
    tmp = []
    with open(os.path.join(turn_dir, tsv), newline='') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in reader:
            wakati_row = []

            for text in row:
                result = jumanpp.analysis(zenhan.h2z(text))
                wakati_text = ' '.join(mrph.midasi for mrph in result.mrph_list())

                wakati_row.append(wakati_text)
            
            tmp.append(wakati_row)
    
    with open(os.path.join(wakati_dir, tsv), 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        writer.writerows(tmp)
