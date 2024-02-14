# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class TutorialSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TutorialDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

import base64
import requests
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from .utils import get_random_dict_from_url
class ProxyMiddleware(HttpProxyMiddleware):
    def process_request(self,request,spider):
        spider.logger.debug('ProxyMiddleware process_request')
        # tunnel = "z277.kdltps.com:15818"
        # username = "xxxxxx"
        # password = "xxxxxx"
        # proxies = {
        #     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        #     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
        # }

        # http://127.0.0.1:8080/get?type=HTTP&count=10&anonymity=all

        proxyDict=get_random_dict_from_url()

        if proxyDict:
            spider.logger.debug('proxyDict {}'.format(proxyDict))
            proxy = proxyDict['Ip']
            port = proxyDict['Port']
            tunnel = proxy + ":" + port
            proxies = {
                "http": "http://%(proxy)s/" % { "proxy": tunnel},
                "https": "http://%(proxy)s/" % { "proxy": tunnel}
            }
            request.meta["proxy"] = proxies['http']
            request.meta["download_timeout"] = 5


from .settings import USER_AGENTS

class HeaderMiddleware(HttpProxyMiddleware):
    def process_request(self,request,spider):
        spider.logger.debug('HeaderMiddleware process_request')
        request.headers['User-Agent'] = random.choice(USER_AGENTS)  # 修改headers


from scrapy import Request
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
import time
from scrapy.exceptions import IgnoreRequest

from .utils import store_url_in_redis

class MyRedirectMiddleware(RedirectMiddleware):
    def process_response(self, request, response, spider):
        spider.logger.info('MyRedirectMiddleware process_response')
        if response.status != 200:
            redis_host = spider.settings.get('REDIS_HOST')
            redis_port = spider.settings.get('REDIS_PORT', 6379)
            redis_db = spider.settings.get('REDIS_DB', 0)
            redis_password = spider.settings.get('REDIS_PASSWORD')
            store_url_in_redis(redis_host, redis_port, redis_db, redis_password,spider.name+":urls",response.url)
            raise IgnoreRequest("Redirect ignored: %s" % response.url)
        return super().process_response(request, response, spider)