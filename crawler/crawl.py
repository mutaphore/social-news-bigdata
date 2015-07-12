from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from crawler.spiders.page_crawler import PageCrawler

def main():
	configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
	process = CrawlerProcess(get_project_settings())
	crawler = PageCrawler()
	process.crawl(crawler)
	process.start()


if __name__ == '__main__':
	main()