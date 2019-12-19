#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from os.path import isfile, join
import regex as re

INPUT_DIRECTORY = './bundler_input/'
OUTPUT_DIRECTORY = './bundler_output/'

# dict for Simplified Chinese to English names for Bible books
hans_eng_bible_books_dict = {
    "创世记": "Genesis",
    "出埃及记": "Exodus",
    "利未记": "Leviticus",
    "民数记": "Numbers",
    "申命记": "Deuteronomy",
    "约书亚记": "Joshua",
    "士师记": "Judges",
    "路得记": "Ruth",
    "撒母耳记上": "1 Samuel",
    "撒母耳记下": "2 Samuel",
    "列王纪上": "1 Kings",
    "列王纪下": "2 Kings",
    "历代志上": "1 Chronicles",
    "历代志下": "2 Chronicles",
    "以斯拉记": "Ezra",
    "尼希米记": "Nehemiah",
    "以斯帖记": "Esther",
    "约伯记": "Job",
    "诗篇": "Psalm",
    "箴言": "Proverbs",
    "传道书": "Ecclesiastes",
    "雅歌": "Song of Solomon",
    "以赛亚书": "Isaiah",
    "耶利米书": "Jeremiah",
    "耶利米哀歌": "Lamentations",
    "以西结书": "Ezekiel",
    "但以理书": "Daniel",
    "何西阿书": "Hosea",
    "约珥书": "Joel",
    "阿摩司书": "Amos",
    "俄巴底亚书": "Obadiah",
    "约拿书": "Jonah",
    "弥迦书": "Micah",
    "那鸿书": "Nahum",
    "哈巴谷书": "Habakkuk",
    "西番雅书": "Zephaniah",
    "哈该书": "Haggai",
    "撒迦利亚书": "Zechariah",
    "玛拉基书": "Malachi",
    "马太福音": "Matthew",
    "马可福音": "Mark",
    "路加福音": "Luke",
    "约翰福音": "John",
    "使徒行传": "Acts",
    "罗马书": "Romans",
    "哥林多前书": "1 Corinthians",
    "哥林多后书": "2 Corinthians",
    "加拉太书": "Galatians",
    "以弗所书": "Ephesians",
    "腓立比书": "Philippians",
    "歌罗西书": "Colossians",
    "帖撒罗尼迦前书": "1 Thessalonians",
    "帖撒罗尼迦后书": "2 Thessalonians",
    "提摩太前书": "1 Timothy",
    "提摩太后书": "2 Timothy",
    "提多书": "Titus",
    "腓利门书": "Philemon",
    "希伯来书": "Hebrews",
    "雅各书": "James",
    "彼得前书": "1 Peter",
    "彼得后书": "2 Peter",
    "约翰一书": "1 John",
    "约翰二书": "2 John",
    "约翰三书": "3 John",
    "犹太书": "Jude",
    "启示录": "Revelation"
}

# dict for Traditional Chinese to English names for Bible books
hant_eng_bible_books_dict = {
    "創世記": "Genesis",
    "出埃及記": "Exodus",
    "利未記": "Leviticus",
    "民數記": "Numbers",
    "申命記": "Deuteronomy",
    "約書亞記": "Joshua",
    "士師記": "Judges",
    "路得記": "Ruth",
    "撒母耳記上": "1 Samuel",
    "撒母耳記下": "2 Samuel",
    "列王紀上": "1 Kings",
    "列王紀下": "2 Kings",
    "歷代志上": "1 Chronicles",
    "歷代志下": "2 Chronicles",
    "以斯拉記": "Ezra",
    "尼希米記": "Nehemiah",
    "以斯帖記": "Esther",
    "約伯記": "Job",
    "詩篇": "Psalm",
    "箴言": "Proverbs",
    "傳道書": "Ecclesiastes",
    "雅歌": "Song of Solomon",
    "以賽亞書": "Isaiah",
    "耶利米書": "Jeremiah",
    "耶利米哀歌": "Lamentations",
    "以西結書": "Ezekiel",
    "但以理書": "Daniel",
    "何西阿書": "Hosea",
    "約珥書": "Joel",
    "阿摩司書": "Amos",
    "俄巴底亞書": "Obadiah",
    "約拿書": "Jonah",
    "彌迦書": "Micah",
    "那鴻書": "Nahum",
    "哈巴谷書": "Habakkuk",
    "西番雅書": "Zephaniah",
    "哈該書": "Haggai",
    "撒迦利亞書": "Zechariah",
    "瑪拉基書": "Malachi",
    "馬太福音": "Matthew",
    "馬可福音": "Mark",
    "路加福音": "Luke",
    "約翰福音": "John",
    "使徒行傳": "Acts",
    "羅馬書": "Romans",
    "哥林多前書": "1 Corinthians",
    "哥林多后書": "2 Corinthians",
    "加拉太書": "Galatians",
    "以弗所書": "Ephesians",
    "腓立比書": "Philippians",
    "歌羅西書": "Colossians",
    "帖撒羅尼迦前書": "1 Thessalonians",
    "帖撒羅尼迦后書": "2 Thessalonians",
    "提摩太前書": "1 Timothy",
    "提摩太后書": "2 Timothy",
    "提多書": "Titus",
    "腓利門書": "Philemon",
    "希伯來書": "Hebrews",
    "雅各書": "James",
    "彼得前書": "1 Peter",
    "彼得后書": "2 Peter",
    "約翰一書": "1 John",
    "約翰二書": "2 John",
    "約翰三書": "3 John",
    "猶太書": "Jude",
    "啟示錄": "Revelation"
}

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
            # use English for Chinese Bible book key
            if "zh-Hans" in fin:
                book = hans_eng_bible_books_dict.get(book)
            elif "zh-Hant" in fin:
                book = hant_eng_bible_books_dict.get(book)

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
