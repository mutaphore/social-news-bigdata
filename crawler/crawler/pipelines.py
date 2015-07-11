# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
from scrapy.exporters import CsvItemExporter, XmlItemExporter

class CrawlerPipeline(object):
    EXPORT_PATH = os.getenv("HOME") + "/Google Drive/Realtime Big Data Analytics/project/code/crawler/"

    def __init__(self):
        self.path = CrawlerPipeline.EXPORT_PATH + 'aggregate.csv'
        self.export_file = open(self.path, 'ab' if os.path.isfile(self.path) else 'wb')
        self.exporter = CsvItemExporter(self.export_file)
        self.exporter.fields_to_export = ["item_id", "url", "headers", "text"]


    def spider_opened(self, spider):
        self.exporter.start_exporting()


    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.export_file.close()


    def process_item(self, item, spider):
        # This is a common path among ALL crawlers
        self.exporter.export_item(item)
        return item
