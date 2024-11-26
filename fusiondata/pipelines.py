# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os
import requests

class FusiondataPipeline:
    def open_spider(self, spider):
        self.file = open('papers.json', 'a', encoding='utf-8')
        self.file.write('[')
        if not os.path.exists('pdfs'):
            os.makedirs('pdfs')
    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

class PubsPipeline:
    def open_spider(self, spider):
        self.file = open('pubs.json', 'a', encoding='utf-8')
        self.file.write('[')

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item
    
class iopPipeline:
    def open_spider(self, spider):
        self.file = open('papers.json', 'a', encoding='utf-8')
        self.file.write('[')

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item
    
class iaeaPipeline:
    def open_spider(self, spider):
        self.file = open('papers.json', 'a', encoding='utf-8')
        self.file.write('[')
        if not os.path.exists('pdfs'):
            os.makedirs('pdfs')
    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item