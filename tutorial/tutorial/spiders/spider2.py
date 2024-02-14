import scrapy
from scrapy.utils.project import get_project_settings
from ..utils  import get_dict_list_from_redis,getCurrentDateString

from ..utils  import get_urls_from_redis,delete_key_from_redis

class Spider2Spider(scrapy.Spider):
    name = "spider2"
    cookies={}

    def __init__(self, list_redis_key=None, param2=None, *args, **kwargs):
            super(Spider2Spider, self).__init__(*args, **kwargs)
            if list_redis_key is None:
                list_redis_key="quotes:"+getCurrentDateString()
            self.list_redis_key = list_redis_key
            self.param2 = param2
            self.logger.debug("list_redis_key ={}".format(self.list_redis_key))
    def start_requests(self):

        settings = get_project_settings()

        self.cookies= settings.get('NGA_COOKIE')


        urls=[]


        redis_host =  settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT')
        redis_db = settings.get('REDIS_DB')
        redis_password = settings.get('REDIS_PASSWORD')




        threadInfos = get_dict_list_from_redis(redis_host, redis_port, redis_db,redis_password, self.list_redis_key)
        for threadItem in threadInfos:
            url = "https://bbs.nga.cn{}".format(threadItem['href'])
            urls.append(url)
            if settings.get('IS_TEST',False):
                 break
        # 处理上次失败的url
        threadInfos = get_urls_from_redis(redis_host, redis_port, redis_db,redis_password, self.name+":urls")
        for threadItem in threadInfos:
            self.logger.debug("threadItem:{}".format(threadItem))
            urls.append(threadItem)
        delete_key_from_redis(redis_host, redis_port, redis_db,redis_password, self.name+":urls")

        max_item_num = settings.get('MAX_ITEM_NUM',0)
        for i in range(len(urls)):
            if max_item_num>0 and i>=max_item_num:
                break
            url = urls[i]
            yield scrapy.Request(url=url,cookies=self.cookies,
 callback=self.parse)


                 

    def parse(self, response):
        for quote in response.css("table.postbox"):
            yield {
                "text": quote.css(".postcontent::text").get(),
                "author_id": quote.css("a.author::attr('href')").get().replace("nuke.php?func=ucp&uid=",""),
                "post_date": quote.xpath('//span[@title="reply time"]/text()').get(),
                "url":response.url,
                "content":response.text
            }
        next_page = response.xpath('//a[@title="下一页"]').xpath('./@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page),cookies=self.cookies, callback=self.parse)
