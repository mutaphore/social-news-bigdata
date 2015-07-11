# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys

class CrawlerPipeline(object):
    path = os.getenv("HOME") + "/Google Drive/Realtime Big Data Analytics/project/code/crawler/"

    def __init__(self):
        self.file = open('aggregate.txt', 'wb')

    def process_item(self, item, spider):
        # This is a common path among ALL crawlers
        # filename = item["url"].split("/")[-2] + '.html'
        # with open(path + filename, 'w') as f:
        #     # f.write(item["url"] + "\n")
        #     # f.write(item["headers"] + "\n")
        self.file.write(item["url"] + "\n")
        self.file.write(item["headers"] + "\n")
        return item
