# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from lesson_avito.settings import mongo_client

class LessonAvitoPipeline(object):
    def process_item(self, item, spider):
        data_base=mongo_client[spider.name]
        collection=data_base[type(item).__name__]
        collection.insert(item)
        return item
