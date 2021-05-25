import csv
import glob
import html
import re

from tqdm import tqdm

screen_name = re.compile(r'((^| )@[a-zA-Z0-9_]{1,15})+($| )')
not_ja = re.compile(r'[^\u0000-\u007f\u3000-\u30ff\u4e00-\u9fff]')
repetition = re.compile(r'(.)\1{4}')

with open('cleaned.tsv', 'w', encoding='utf-8') as f:
    pass

n_raw = 0
n_written = 0

tsvs = sorted(glob.glob('tsvs/*.tsv'))

for tsv in tqdm(tsvs):
    with open(tsv, encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in reader:
            full_texts = []
            n_raw += 1

            for full_text in row:
                full_text = html.unescape(full_text)
                full_text = screen_name.sub('', full_text)

                if not_ja.search(full_text):
                    break
                if repetition.search(full_text):
                    break
                if len(full_text) < 4:
                    break

                full_texts.append(full_text)

            else:
                with open('cleaned.tsv', 'a', encoding='utf-8') as g:
                    g.write('\t'.join(full_texts) + '\n')
                
                n_written += 1

print(f'Write {n_written} dialogues: {n_written / n_raw:%} of the total')
