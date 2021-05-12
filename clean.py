import csv
import glob
import re
import sys

screen_name = re.compile(r'@[a-zA-Z0-9_]{1,15}')

ja = re.compile(r'[\u0000-\u007f\u3000-\u30ff\u4e00-\u9fff]+')
repetition = re.compile(r'(.)\1{4}')

with open('cleaned.tsv', 'w', encoding='utf-8') as f:
    pass

tsvs = sorted(glob.glob('tsvs/*.tsv'))
n_dialogues = 0

n_orig = 0

for tsv in tsvs:
    with open(tsv, encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in reader:
            n_orig += 1

            full_texts = []

            for full_text in row:
                full_text = full_text.rstrip()

                while screen_name.match(full_text):
                    full_text = screen_name.sub('', full_text).strip()

                if not ja.fullmatch(full_text):
                    break
                
                if repetition.search(full_text):  # more than 4 times
                    break

                if len(full_text) < 4:  # less than 4 characters
                    break

                full_texts.append(full_text)

            else:
                with open('cleaned.tsv', 'a', encoding='utf-8') as g:
                    g.write('\t'.join(full_texts) + '\n')
                
                n_dialogues += 1

print(f'Write {n_dialogues} dialogues: {n_dialogues / n_orig:%} of the total')
