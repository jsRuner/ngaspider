from pathlib import Path
import scrapy

from scrapy.utils.project import get_project_settings

from ..utils  import get_urls_from_redis,delete_key_from_redis

import time

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    custom_delay = 1  # 初始延迟时间（单位：秒）

    cookies={}
    def __init__(self, fid=None, param2=None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        if fid is None:
            fid = 510428
        
        self.fid = fid
        self.param2 = param2

    def start_requests(self):
        settings = get_project_settings()
        redis_host =  settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT')
        redis_db = settings.get('REDIS_DB')
        redis_password = settings.get('REDIS_PASSWORD')

        self.cookies= settings.get('NGA_COOKIE')

        urls = []
        self.logger.debug("fid:{}".format(self.fid))
        for i in range(1, 2):
            urls.append("https://bbs.nga.cn/thread.php?fid={}&order_by=postdatedesc&page={}".format(self.fid,i))
        # 处理上次失败的url
        threadInfos = get_urls_from_redis(redis_host, redis_port, redis_db,redis_password, self.name+":urls")
        for threadItem in threadInfos:
            self.logger.debug("threadItem:{}".format(threadItem))
            urls.append(threadItem)
        delete_key_from_redis(redis_host, redis_port, redis_db,redis_password, self.name+":urls")



        for url in urls:
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
                "content":response.text
            }
        
        next_page = response.xpath('//a[@title="下一页"]').xpath('./@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page),cookies=self.cookies, callback=self.parse)

