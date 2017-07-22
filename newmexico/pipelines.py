# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.exceptions import DropItem
import logging
from scrapy.conf import settings

class MongoDBPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings['MONGO_URI']
        )
        
        db = connection[settings['MONGO_DATABASE']]
        self.collection = db[settings['MONGO_COLLECTION']]
        self.collection.create_index('PropertyCode', unique=True)

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
                logging.info('Property was missing {0}'.format(data))
        if valid:
            self.collection.update(dict(item), upsert=True)
            logging.info("Property added to MongoDB database!")
        return item
