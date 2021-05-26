import argparse
import csv
import glob
import html
import re
from collections import defaultdict

from tqdm import tqdm

screen_name = re.compile(r'((^| )@[a-zA-Z0-9_]{1,15})+($| )')
not_ja = re.compile(r'[^\u0000-\u007f\u3000-\u30ff\u4e00-\u9fff]')
repetition = re.compile(r'(.)\1{4}')

parser = argparse.ArgumentParser()
parser.add_argument('raw_dir')
parser.add_argument('turn_dir')
parser.add_argument('--sub', action='store_true')
args = parser.parse_args()

turn_to_dialogues = defaultdict(list)

n_read = 0
n_written = 0

tsvs = glob.glob(f'{args.raw_dir}/*.tsv')

for tsv in tqdm(tsvs):
    with open(tsv, encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

        for row in reader:
            full_texts = []
            n_read += 1

            for full_text in row:
                full_text = html.unescape(full_text)
                full_text = screen_name.sub('', full_text)

                if args.sub:
                    full_text = ' '.join(not_ja.sub('', full_text).split())
                elif not_ja.search(full_text):
                    break
                
                if repetition.search(full_text):
                    break
                if len(full_text) < 4:
                    break

                full_texts.append(full_text)

            else:
                turn_to_dialogues[len(full_texts)].append(full_texts)
                n_written += 1

for turn, dialogues in turn_to_dialogues.items():
    with open(f'{args.turn_dir}/{turn}.tsv', 'w', encoding='utf-8') as f:
        for dialogue in dialogues:
            f.write('\t'.join(dialogue) + '\n')

print(f'Write {n_written} dialogues: {n_written / n_read:%} of the total')
