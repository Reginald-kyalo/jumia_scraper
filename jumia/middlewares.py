#from urllib.parse import urlencode
#
#class ScrapingBeeMiddleware:
#    def __init__(self, api_key):
#        self.api_key = api_key
#
#    @classmethod
#    def from_crawler(cls, crawler, *args, **kwargs):
#        api_key = crawler.settings.get('SCRAPINGBEE_API_KEY')
#        return cls(api_key)
#
#    def process_request(self, request, spider):
#        # Create the ScrapingAnt API URL with the request URL
#        payload = {
#            'api_key': os.getenv("SCRAPINGBEE_API_KEY"),
#            'url': request.url,
#            'render_js': 'false'
#        }
#        proxy_url = 'https://app.scrapingbee.com/api/v1?' + urlencode(payload)
#        return request.replace(url=proxy_url, meta={'proxy_used': True})
#payload = {
#    'url': 'https://www.jumia.co.ke/catalog/?q=iphone',
#    'x-api-key': os.getenv("SCRAPINGANT_API_KEY"),
#}
#proxy_url = 'https://api.scrapingant.com/v2/general?' + urlencode(payload)
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import logging

class SpiderTimingMiddleware:
    def __init__(self, stats):
        self.stats = stats
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        # Create an instance of the middleware with access to stats
        middleware = cls(crawler.stats)
        # Connect signals
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        self.logger.info(f"Spider {spider.name} started.")

    def spider_closed(self, spider, reason):
        stats = self.stats.get_stats()
        start_time = stats.get("start_time")
        finish_time = stats.get("finish_time")

        if start_time and finish_time:
            duration = (finish_time - start_time).total_seconds()
            self.logger.info(f"Spider {spider.name} ran for {duration:.2f} seconds. Reason: {reason}")
class SpiderMiddleware:
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
        spider.logger.info('Spider opened: %s' % spider.name)


class DownloaderMiddleware:
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
        spider.logger.info('Spider opened: %s' % spider.name)
