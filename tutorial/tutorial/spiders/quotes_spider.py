from pathlib import Path
import scrapy

from scrapy.utils.project import get_project_settings

from ..utils  import get_urls_from_redis,delete_key_from_redis

import time

class QuotesSpider(scrapy.Spider):
    name = "quotes"


    cookies={}
    def __init__(self, fid=None, pages=None,mode=None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.logger.debug('fid: %s, pages: %s,mode:%s' % (fid, pages,mode))
        if fid is None:
            fid = 510428
        if pages is None:
            pages = 335
            #0 从新开始 1 处理上次失败的url
        if mode is None:
            mode = '0'

        
        
        self.fid = fid
        self.pages = pages
        self.mode = mode


    def start_requests(self):
        settings = get_project_settings()
        redis_host =  settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT')
        redis_db = settings.get('REDIS_DB')
        redis_password = settings.get('REDIS_PASSWORD')

        self.cookies= settings.get('NGA_COOKIE')

        urls = []
        if self.mode == '0':
            for i in range(1, self.pages):
                urls.append("https://bbs.nga.cn/thread.php?fid={}&order_by=postdatedesc&page={}".format(self.fid,i))
        if self.mode == '1':
            threadInfos = get_urls_from_redis(redis_host, redis_port, redis_db,redis_password, self.name+":urls")
            for threadItem in threadInfos:
                self.logger.debug("threadItem:{}".format(threadItem))
                urls.append(threadItem)
            delete_key_from_redis(redis_host, redis_port, redis_db,redis_password, self.name+":urls")

        self.logger.debug("urls:{}".format(urls))
        max_item_num = settings.get('MAX_ITEM_NUM',0)
        for i in range(len(urls)):
            if max_item_num>0 and i>=max_item_num:
                break
            url = urls[i]
            yield scrapy.Request(url=url,cookies=self.cookies,
 callback=self.parse)

    def parse(self, response):
        for quote in response.css("tr.topicrow"):
            yield {
                "text": quote.css(".topic::text").get(),
                "author_name": quote.css(".author::text").get(),
                "author_id": quote.css(".author::attr(title)").get().replace("用户ID ", ""),
                "href": quote.css(".topic::attr(href)").get(),
                "fid":self.fid,
                "post_date": quote.css("span.postdate::text").get(),
                "replyer_name": quote.css(".replyer::text").get(),
                "replies": quote.css(".replies::text").get(),
                "url":response.url,
            }
        
       
