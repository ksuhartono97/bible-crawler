# bible-crawler
Simple python script to crawl (https://www.biblegateway.com/). Currently works for bible versions that supply a direct mapping between verse and verse number (i.e. doesn't work for MSG translation)

Tested on Macbook Pro running MacOS Mojave version 10.14.4. 

Environment information:
- Python 3.6.5 
- Scrapy 1.7.1

## Installation
To install dependencies, run:
```
pip install -r requirements.txt
```

## Usage
```
scrapy runspider spider.py -o [FILENAME].json
```

Replace `FILENAME` with any name you want the json output to be stored in. Change the start link in the script to Genesis 1 in your desired version. 
