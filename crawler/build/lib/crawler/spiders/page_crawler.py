import sys
import os
import re

import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup

from crawler.items import CrawlerItem

class PageCrawler(scrapy.Spider):
    """A generic crawler that scrapes text and other stuff from webpages"""
    name = "spider1"
    start_urls = []
    DEFAULT_URLS_FILE = "/Users/deweichen/Google Drive/Realtime Big Data Analytics/project/code/crawler/urls.txt"
    DEFAULT_SPIDER_ID = "myspider"
    #following can be omitted if we use start_requests
    # start_urls = [
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
        # "http://sauravtom.tumblr.com/post/123807612560/oldest-surviving-melody-in-history",
        # "http://backreaction.blogspot.com/2015/06/no-gravity-hasnt-killed-schrodingers-cat.html",
        # "http://jacquesmattheij.com/if-you-have-nothing-to-hide",
    # ]

    def __init__(self, spider_id=None, urls_file=None, *args, **kwargs):
        super(PageCrawler, self).__init__(*args, **kwargs)
        # Initialize spider id argument if there is one
        self.spider_id = spider_id if spider_id else PageCrawler.DEFAULT_SPIDER_ID
        self.urls_file = urls_file if urls_file else PageCrawler.DEFAULT_URLS_FILE


    def get_text(self, soup):
        "Given soup, do preliminary cleans and return the text"
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
        "This will yield new urls from the urls file"
        with open(self.urls_file, 'r') as urls:
            for url in urls:
                yield Request(url, self.parse)


    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        # save item
        item = CrawlerItem()
        #TODO: filename needs to be an id so we can grab it later
        item["item_id"] = "1"
        item["url"] = str(response.url)
        item["headers"] = str(response.headers)
        item["num_links"] = len(soup.find_all('a'))
        item["num_images"] = len(soup.find_all('img'))
        item["num_scripts"] = len(soup.find_all('script'))
        item["num_styles"] = len(soup.find_all('style'))
        item["text"] = self.get_text(soup)
        yield item
