# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os

class TutorialPipeline:
    def process_item(self, item, spider):
        return item

# 清理版面
class DelThreadPipeline:
    def process_item(self, item, spider):
        if "read.php" not in item['href']:
            return None
        else:
            return item
    
from .utils import filter_chinese
class OnlyKeepCnPipeline:
    def process_item(self, item, spider):

        

        text = item['text']
        # text1 = item['text1']
        # if text is None and text1:
        #     text = text1
        # if text is None:
        #     print("text is none {}".format(item))
        item['text'] = filter_chinese(text)


        return item



    def get_filename_from_url(self, url):
        import re
        # 从URL中提取文件名
        # 实现根据需要进行具体的文件名提取逻辑
        filename = '1.html'

        


        pattern = r"page=(\d+)"
        match = re.search(pattern, url)
        if match:
            page_number = int(match.group(1))
            filename = "{}.html".format(page_number)

        return filename
    
import redis
import json
from datetime import datetime

class MyRedisPipeline(object):
    def __init__(self, redis_host, redis_port, redis_password, redis_key):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.redis_key = redis_key

    @classmethod
    def from_crawler(cls, crawler):
        redis_host = crawler.settings.get('REDIS_HOST')
        redis_port = crawler.settings.get('REDIS_PORT', 6379)
        redis_password = crawler.settings.get('REDIS_PASSWORD')

        

        
        current_time = datetime.now()
        time_string = current_time.strftime("%Y%m%d%")

        redis_key = "{}:{}".format(crawler.spider.name,time_string)

        return cls(redis_host, redis_port, redis_password, redis_key)

    def open_spider(self, spider):
        self.redis_client = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password
        )

    def close_spider(self, spider):
        self.redis_client.connection_pool.disconnect()

    def process_item(self, item, spider):
        # 处理结果并存储到Redis的指定键中
        self.redis_client.lpush(self.redis_key, json.dumps(item,ensure_ascii=False))
        return item