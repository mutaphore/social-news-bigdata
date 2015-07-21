import sys
import os
import re
import csv

import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup

from crawler.items import CrawlerItem

class PageCrawler(scrapy.Spider):
    """A generic crawler that scrapes text and other stuff from webpages"""
    DEFAULT_URLS_FILE = "urls.txt"
    DEFAULT_SPIDER_ID = "spider1"
    name = "spider1"
    start_urls = []

    def __init__(self, spider_id=None, urls_file=None, *args, **kwargs):
        "Initialize spider arguments"
        super(PageCrawler, self).__init__(*args, **kwargs)
        self.spider_id = spider_id if spider_id else PageCrawler.DEFAULT_SPIDER_ID
        self.urls_file = urls_file if urls_file else PageCrawler.DEFAULT_URLS_FILE
        self.news_site = news_site if news_site else "hackernews"


    def get_text(self, soup):
        "Given soup object, do preliminary cleans and return the text parsed"
        # remove all script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        soup = BeautifulSoup(soup.prettify(), "lxml")
        text = soup.get_text(" ", strip=True)

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)
        # encode to utf-8
        return text.encode("utf-8")


    def start_requests(self):
        "This function creates new requests for the spider from the urls file"
        ext = os.path.splitext(self.urls_file)[-1].lower()
        with open(self.urls_file, 'r') as input_file:
            if ext == '.csv':
                reader = csv.DictReader(input_file)
                for row in reader:
                    #check type is 'story', for hackernews API only
                    if row['type'] == 'story' and row['url']:
                        yield Request(row['url'], self.parse, meta={'item_id': row['id']})
            else:
                for line in input_file:
                    if line:
                        yield Request(line.strip(), self.parse)


    def parse(self, response):
        "Parse response attributes into item"
        soup = BeautifulSoup(response.body, "lxml")
        # save item fields
        item = CrawlerItem()
        #TODO: filename needs to be an id so we can grab it later
        item["item_id"] = response.meta['item_id']
        item["url"] = str(response.url)
        item["headers"] = str(response.headers)
        item["num_links"] = len(soup.find_all('a'))
        item["num_images"] = len(soup.find_all('img'))
        item["num_scripts"] = len(soup.find_all('script'))
        item["num_styles"] = len(soup.find_all('style'))
        item["text"] = self.get_text(soup)
        yield item
