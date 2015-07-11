import sys
import os
import re

import scrapy
from bs4 import BeautifulSoup

from crawler.items import CrawlerItem

class PageCrawler(scrapy.Spider):
    """A generic crawler that scrapes text and other stuff from webpages"""
    name = "pagecrawler"
    start_urls = [
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
        # "http://sauravtom.tumblr.com/post/123807612560/oldest-surviving-melody-in-history",
        # "http://backreaction.blogspot.com/2015/06/no-gravity-hasnt-killed-schrodingers-cat.html",
        "http://jacquesmattheij.com/if-you-have-nothing-to-hide",
    ]

    def set_instance_id(self, instance_id):
        self.instance_id = instance_id


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