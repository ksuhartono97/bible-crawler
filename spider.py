import scrapy
import regex as re

class BibleSpider(scrapy.Spider):
    name = 'biblespider'
    start_urls = ['https://www.biblegateway.com/passage/?search=Genesis+1&version=NASB']
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'LOG_LEVEL' : 'INFO'
    }

    def is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def parse(self, response):
        # print("Existing settings: %s" % self.settings.attributes.keys())

        # Get book and chapter number
        book_and_chapter = response.css('.passage-display-bcv').css('span::text').get()
        temp = book_and_chapter.rsplit(' ', 1)
        if len(temp) > 1:
            if(self.is_number(temp[1])):
                book = temp[0]
                chapternum = temp[1]
            else:
                book = book_and_chapter
                chapternum = ""
        else:
            book = book_and_chapter
            chapternum = ""
        
        # Clean up input
        book = book.strip()
        chapternum = chapternum.strip()
        chapternum = re.sub("[^0-9]", "", chapternum)
        chapternum = '1' if chapternum == "" else chapternum
        
        chapterText = " "
        
        # Get part of page where passage is shown
        passagediv = response.xpath("//div[@class='passage-wrap']")
        
        # Flag to detect if this is first verse as first verse has no verse number
        foundVerseNum = False

        # Find verses in passage
        for passage in passagediv.css('span.text'):
            # Get the verse number if it exists in current html element
            verseNum = passage.css('sup.versenum::text').get()
            if verseNum is not None:
                chapterText += " "
                chapterText += verseNum
                foundVerseNum = True

            # Special case for special titles
            # for v in passage.xpath("./text()[ancestor::h3]"):
            #     chapterText += "999\xa0"
            #     chapterText += v.get()
            
            # Eliminate unnecessary 
            for v in passage.xpath(".//text()[not(ancestor::*[@class='chapternum']) \
                and not(ancestor::h3) and not(ancestor::sup)]"):
                if not foundVerseNum:
                    chapterText += " "
                    chapterText += "1\xa0"
                    foundVerseNum = True

                # Whitespace editing for clarity
                chapterText += ' '
                chapterText += v.get().strip()

        # Create dict of verse number and verse text
        splitted_verses = re.split("\s\w*\xa0", chapterText)
        verse_numbers = re.findall("\s\w*\xa0", chapterText)
        for i in range(len(verse_numbers)):
            verse_numbers[i] = re.sub("[^0-9]", "", verse_numbers[i])
        verse_dict = dict()
        for i in range(len(splitted_verses)):
            if i == 0:
                continue
            verse_dict.update({verse_numbers[i-1].strip() : splitted_verses[i].strip()})

        # Yield the result of this chapter
        yield {
            'book': book,
            'chapter': chapternum,
            'verses': verse_dict
        }

        # Find next chapter
        next_page = response.css('div.next-chapter a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)