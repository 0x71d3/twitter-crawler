import csv
import glob
import re
import sys

ja = re.compile(r'[\u0000-\u007f\u3000-\u30ff\u4e00-\u9fff]+')
screen_name = re.compile(r'@[a-zA-Z0-9_]{1,15}')

with open('cleaned.tsv', 'w', encoding='utf-8') as f:
    pass

for tsv in sorted(glob.glob('tsvs/*.tsv')):
    with open(tsv, encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in reader:
            full_texts = []

            for full_text in row:
                full_text = full_text.rstrip()

                while screen_name.match(full_text):
                    full_text = screen_name.sub('', full_text).strip()

                if not ja.fullmatch(full_text):
                    break
                    
                full_texts.append(full_text)

            else:
                with open('cleaned.tsv', 'a', encoding='utf-8') as f:
                    f.write('\t'.join(full_texts) + '\n')
