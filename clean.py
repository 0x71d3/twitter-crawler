import argparse
import csv
import glob
import html
import re
from collections import defaultdict

from tqdm import tqdm

screen_name = re.compile(r'@[A-Za-z0-9_]{1,15}')
parentheses = re.compile(r'\(.*?\)')

ja = re.compile(r'[\u3000-\u30ff\u4e00-\u9fff]')

not_ja = re.compile(r'[^\u3000-\u30ff\u4e00-\u9fff]')
not_ascii_nor_ja = re.compile(r'[^\u0000-\u007f\u3000-\u30ff\u4e00-\u9fff]')

min_length = 4
repetition = re.compile(r'(.+)\1{4}')


def main(args):
    turn_to_dialog = defaultdict(set)
    n_read = 0

    tsvs = glob.glob(f'{args.data_dir}/*.tsv')
    for tsv in tqdm(tsvs):
        with open(tsv, encoding='utf-8', newline='') as f:
            reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

            for row in reader:
                texts = []

                for text in row:
                    text = html.unescape(text)
                    text = screen_name.sub('', text)
                    text = ' '.join(text.split())

                    if not ja.search(text):  # at least
                        break

                    if args.sub:
                        if args.ascii:
                            text = not_ascii_nor_ja.sub('', text)
                        else:
                            text = not_ja.sub('', text)

                        text = parentheses.sub('', text)  # parentheses
                        text = ' '.join(text.split())

                    else:
                        if args.ascii:
                            if not_ascii_nor_ja.search(text):
                                break
                        else:
                            if not_ja.search(text):
                                break
                    
                    if len(text) < min_length:  # length
                        break

                    if repetition.search(text):  # repetition
                        break

                    texts.append(text)

                else:
                    turn_to_dialog[len(texts)].add('\t'.join(texts))

                n_read += 1

    n_written = 0

    for n_turns, dialogs in turn_to_dialog.items():
        with open(f'{args.output_dir}/{n_turns}.tsv', 'w', encoding='utf-8') as f:
            f.write('\n'.join(dialogs) + '\n')
            n_written += len(dialogs)

    print(f'Write {n_written} dialogues: {n_written / n_read:%} of the total')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('data_dir')
    parser.add_argument('output_dir')
    parser.add_argument('--ascii', action='store_true')
    parser.add_argument('--sub', action='store_true')

    args = parser.parse_args()

    main(args)
