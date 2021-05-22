import csv
import html
import os
import re

from tqdm import tqdm

screen_name = re.compile(r'(^| )@[a-zA-Z0-9_]{1,15}($| )')

# not_ja = re.compile(r'[^\u0000-\u007f\u3000-\u30ff\u4e00-\u9fff]')
not_ja = re.compile(r'[^ \u3000-\u30ff\u4e00-\u9fff]')

repetition = re.compile(r'(.)\1{4}')

src_dir = 'tsvs'
dst_dir = 'sub'

n_raw = 0
n_written = 0

for tsv in tqdm(os.listdir(src_dir)):
    dialogues = []
    
    with open(os.path.join(src_dir, tsv), encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in reader:
            n_raw += 1

            full_texts = []

            for full_text in row:
                full_text = html.unescape(full_text)

                full_text = screen_name.sub('', full_text)

                full_text = ' '.join(not_ja.sub('', full_text).split())

                if repetition.search(full_text):  # more than 4 times
                    break

                if len(full_text) < 4:  # less than 4 characters
                    break

                full_texts.append(full_text)

            else:
                dialogues.append('\t'.join(full_texts))

                n_written += 1

    with open(os.path.join(dst_dir, tsv), 'w', encoding='utf-8') as f:
        f.write('\n'.join(dialogues) + '\n')

print(f'Write {n_written} dialogues: {n_written / n_raw:%} of the total')
