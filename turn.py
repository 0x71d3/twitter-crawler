import csv
import glob
import os
import re
from collections import defaultdict

screen_name = re.compile(r'@[a-zA-Z0-9_]{1,15}')

ja = re.compile(r'[\u0000-\u007f\u3000-\u30ff\u4e00-\u9fff]+')
repetition = re.compile(r'(.)\1{4}')

turn_to_dialogues = defaultdict(list)

n_total = 0
n_dialogues = 0

tsvs = sorted(glob.glob('tsvs/*.tsv'))

for tsv in tsvs:
    with open(tsv, encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in reader:
            n_total += 1

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
                turn_to_dialogues[len(full_texts)].append(full_texts)
                
                n_dialogues += 1

for turn, dialogues in turn_to_dialogues.items():
    with open(os.path.join('cleaned', f'{turn}.tsv'), 'w', encoding='utf-8') as f:
        for dialogue in dialogues:
            f.write('\t'.join(dialogue) + '\n')

print(f'Write {n_dialogues} dialogues: {n_dialogues / n_total:%} of the total')
