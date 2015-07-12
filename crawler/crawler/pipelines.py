# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys

from scrapy import signals
from scrapy.exporters import CsvItemExporter, XmlItemExporter

class CrawlerPipeline(object):
    EXPORT_PATH = os.getenv("HOME") + "/Google Drive/Realtime Big Data Analytics/project/code/crawler/"

    def __init__(self):
        self.files = {}


    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline


    def spider_opened(self, spider):
        path = CrawlerPipeline.EXPORT_PATH + spider.spider_id + '_export.csv'
        export_file = open(path, 'ab' if os.path.isfile(path) else 'wb')

        self.files[spider.spider_id] = export_file
        self.exporter = CsvItemExporter(export_file)
        self.exporter.fields_to_export = [
            "item_id", "url", "num_links", "num_images", 
            "num_scripts", "num_styles", "headers", "text"
        ]
        self.exporter.start_exporting()


    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        export_file = self.files.pop(spider.spider_id)
        export_file.close()


    def process_item(self, item, spider):
        # This is a common path among ALL crawlers
        self.exporter.export_item(item)
        return item
