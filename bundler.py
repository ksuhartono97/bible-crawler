import json
import os
from os.path import isfile, join
import regex as re

INPUT_DIRECTORY = './bundler_input/'
OUTPUT_DIRECTORY = './bundler_output/'

try:
    os.makedirs(OUTPUT_DIRECTORY)
except FileExistsError:
    # directory already exists
    pass

# Get all files in input directory
files = [f for f in os.listdir(INPUT_DIRECTORY) if isfile(join(INPUT_DIRECTORY, f))]

# Process each file and bundle them together
for f in files:
    fin = join(INPUT_DIRECTORY, f)
    fout = join(OUTPUT_DIRECTORY, f)

    if re.match("(.*?)+(.json)$", fin):
        with open(fin, 'r') as f:
            bible_dict = json.load(f)

        bundled_bible= dict()

        for i in range(len(bible_dict)):
            book = bible_dict[i]['book']
            chapter = bible_dict[i]['chapter']
            verses = bible_dict[i]['verses']

            book_key_value = bundled_bible.setdefault(book, dict())
            book_key_value.update({chapter : verses})
            bundled_bible[book] = book_key_value

        # Try to delete existing files
        try:
            os.remove(fout)
        except Exception: 
            pass

        # Create output
        with open(fout, 'w') as outfile:
            json.dump(bundled_bible, outfile)
