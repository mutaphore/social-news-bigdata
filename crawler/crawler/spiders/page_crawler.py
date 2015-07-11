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
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
        # "http://sauravtom.tumblr.com/post/123807612560/oldest-surviving-melody-in-history"
    ]

    def get_text(self, soup):
        "Given soup, do preliminary cleans and return the text"
        # remove all script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        soup = BeautifulSoup(soup.prettify(), "lxml")
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)
        # encode to utf-8
        return text.encode("utf-8")


    def get_num_links(self, soup):
        "Return number of links on the page"
        a_tags = soup.find_all('a')
        links = [link.get('href') for link in a_tags]
        return len(links)


    def get_num_images(self, soup):
        "Return number of images on the page"
        img_tags = soup.find_all('img')
        return len(img_tags)


    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        #TODO: filename needs to be an id so we can grab it later
        # save item
        item = CrawlerItem()
        item["item_id"] = 1
        item["url"] = str(response.url)
        item["headers"] = str(response.headers)
        item["text"] = self.get_text(soup)
        item["num_links"] = self.get_num_links(soup) 
        item["num_images"] = self.get_num_images(soup) 
        yield item