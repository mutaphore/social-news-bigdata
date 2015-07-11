from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from crawler.spiders.page_crawler import PageCrawler

def main():
	configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
	process = CrawlerProcess(get_project_settings())
	crawler1 = PageCrawler()
	crawler1.set_instance_id("spider1")
	crawler2 = PageCrawler()
	crawler2.set_instance_id("spider2")
	process.crawl(crawler1)
	process.crawl(crawler2)
	process.start()


if __name__ == '__main__':
	main()