import scrapy

class PageCrawler(scrapy.Spider):
    name = "pagecrawler"
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        f = open(filename, 'w')
        f.write(response.body)
        f.close()