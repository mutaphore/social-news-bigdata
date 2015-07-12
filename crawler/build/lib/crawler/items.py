# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
	# Fields for this item
    item_id = scrapy.Field()
    url = scrapy.Field()
    headers = scrapy.Field()
    text = scrapy.Field()
    num_links = scrapy.Field()
    num_images = scrapy.Field()
    num_scripts = scrapy.Field()
    num_styles = scrapy.Field()
