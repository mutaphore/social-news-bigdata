import scrapy
from bs4 import BeautifulSoup
import re

class PageCrawler(scrapy.Spider):
    name = "pagecrawler"
    start_urls = [
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
        "http://www.yahoo.com"
    ]

    def clean_text(self, soup):
        "Given soup, clean it and return the text"
        # kill all script and style elements
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

    def get_links(self, soup):
        "Return a list of urls on the page"
        a_tags = soup.find_all('a')
        links = [link.get('href') for link in a_tags]
        links = [link for link in links if link != "#"]
        return links

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        soup = BeautifulSoup(response.body, "lxml")
        links = self.get_links(soup) 
        text = self.clean_text(soup)
        with open(filename, 'w') as f:
            f.write(str(response.headers) + "\n")
            f.write(str(response.meta) + "\n")
            f.write("\n".join(links))
            f.write(text)