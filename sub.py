import csv
import html
import os
import re

from tqdm import tqdm

screen_name = re.compile(r'((^| )@[a-zA-Z0-9_]{1,15})+($| )')
not_ja = re.compile(r'[^\u0000-\u007f\u3000-\u30ff\u4e00-\u9fff]')
repetition = re.compile(r'(.)\1{4}')

tsv_dir = 'tsvs'
sub_dir = 'sub'

n_raw = 0
n_written = 0

for tsv in tqdm(os.listdir(tsv_dir)):
    tmp = []
    
    with open(os.path.join(tsv_dir, tsv), encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in reader:
            full_texts = []
            n_raw += 1

            for full_text in row:
                full_text = html.unescape(full_text)
                full_text = screen_name.sub('', full_text)

                full_text = ' '.join(not_ja.sub('', full_text).split())

                if repetition.search(full_text):
                    break
                if len(full_text) < 4:
                    break

                full_texts.append(full_text)

            else:
                tmp.append('\t'.join(full_texts))

                n_written += 1

    with open(os.path.join(sub_dir, tsv), 'w', encoding='utf-8') as f:
        f.write('\n'.join(tmp) + '\n')

print(f'Write {n_written} dialogues: {n_written / n_raw:%} of the total')
