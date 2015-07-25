import sys
import os
import re
import csv
import urlparse

import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

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
        self.url_validator = URLValidator()


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


    def clean_url(self, url):
        "Clean a url"
        url = url.strip()
        #check the black list
        if not url or url[-4:].lower() in (".pdf", ".jpg", ".png", ".gif", ".tif"):
            return ""
        #validate the url
        try:
            self.url_validator(url)
        except:
            return ""
        r1 = urlparse.urlsplit(url)
        cleaned_url = r1.geturl()
        return cleaned_url


    def start_requests(self):
        "This function creates new requests for the spider from the urls file"
        ext = os.path.splitext(self.urls_file)[-1].lower()
        with open(self.urls_file, 'rU') as input_file:
            if ext == '.csv':
                dialect = csv.Sniffer().sniff(input_file.read(1024))
                input_file.seek(0)
                reader = csv.DictReader(input_file, dialect=dialect)
                for row in reader:
                    cleaned_url = self.clean_url(row['url'])
                    if cleaned_url:
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
