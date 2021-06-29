import argparse
import csv
import glob
import html
import re
from collections import defaultdict

from tqdm import tqdm

screen_name = re.compile(r'@[A-Za-z0-9_]{1,15}')
parentheses = re.compile(r'\(.*?\)')

ja_chr = re.compile(r'[\u0000-\u007f\u3000-\u30ff\u4e00-\u9fff]')
not_ja_chr = re.compile(r'[^\u0000-\u007f\u3000-\u30ff\u4e00-\u9fff]')

# ja_chr = re.compile(r'[\u3000-\u30ff\u4e00-\u9fff]')
# not_ja_chr = re.compile(r'[^\u3000-\u30ff\u4e00-\u9fff]')

min_length = 4
repetition = re.compile(r'(.+)\1{4}')


def main(args):
    turn_to_dialog = defaultdict(list)

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
                    full_text = ' '.join(full_text.split())

                    if not ja_chr.search(full_text):  # at least
                        break

                    if args.sub:
                        full_text = not_ja_chr.sub('', full_text)
                        full_text = parentheses.sub('', full_text)
                        full_text = ' '.join(full_text.split())

                    elif not_ja_chr.search(full_text):
                        break
                    
                    if len(full_text) < min_length:  # length
                        break

                    if repetition.search(full_text):  # repetition
                        break

                    full_texts.append(full_text)

                else:
                    turn_to_dialog[len(full_texts)].append(full_texts)
                    n_written += 1

    for n_turns, dialogs in turn_to_dialog.items():
        with open(f'{args.output_dir}/{n_turns}.tsv', 'w', encoding='utf-8') as f:
            for dialog in dialogs:
                f.write('\t'.join(dialog) + '\n')

    print(f'Write {n_written} dialogues: {n_written / n_read:%} of the total')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('raw_dir')
    parser.add_argument('output_dir')
    parser.add_argument('--sub', action='store_true')

    args = parser.parse_args()

    main(args)
