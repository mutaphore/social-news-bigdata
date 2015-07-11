import sys
import os
import re

import scrapy
from bs4 import BeautifulSoup

from crawler.items import CrawlerItem

class PageCrawler(scrapy.Spider):
    """A generic crawler that scrapes text and other stuff from webpages"""
    name = "pagecrawler"
    output_path = os.getenv("HOME") + 
        "/Google Drive/Realtime Big Data Analytics/project/code/crawler"
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
        # "http://sauravtom.tumblr.com/post/123807612560/oldest-surviving-melody-in-history"
    ]

    def clean_text(self, soup):
        "Given soup, clean it and return the text"
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
        # save content info for this page
        CrawlerItem.url = response.url
        CrawlerItem.num_links = self.get_num_links(soup) 
        CrawlerItem.num_images = self.get_num_images(soup) 
        # write html text out to file
        text = self.clean_text(soup)
        #TODO: filename needs to be an id so we can grab it later
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'w') as f:
            f.write(str(response.headers) + "\n")
            f.write(str(response.meta) + "\n")
            f.write(text)