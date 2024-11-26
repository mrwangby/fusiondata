# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random
import time
from fake_useragent import UserAgent  # 修正导入
from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest
from scrapy import signals

class ResponseFilterMiddleware:
    def process_response(self, request, response, spider):
        """
        过滤包含特定 HTML/JavaScript 代码的响应，并重发请求
        """
        # 转换响应内容为字符串进行匹配
        body = response.body.decode('utf-8', errors='ignore')

        # 检查是否包含特定的 HTML/JavaScript 代码（例如 <script>）
        if "<script type=\"text/javascript\">" in body and "function leastFactor" in body:
            spider.logger.info(f"Detected unwanted JavaScript in response: {response.url}, retrying...")
            
            # 增加 retry 次数限制，防止无限重发
            if request.meta.get('retry_times', 0) >= 3:  # 限制重试次数为 3 次
                spider.logger.warning(f"Max retries reached for {response.url}, discarding response.")
                raise IgnoreRequest()  # 丢弃该请求
            
            # 增加 retry 次数，并返回新的请求对象
            request.meta['retry_times'] = request.meta.get('retry_times', 0) + 1
            return request.copy()

        # 如果不匹配，返回正常的响应对象
        return response

    def process_exception(self, request, exception, spider):
        """
        捕获异常时的逻辑（可选）
        """
        spider.logger.error(f"Exception occurred: {exception}")
        return None  # 不处理异常，交给其他中间件

class ProxyDownloaderMiddleware:
    _proxy = ('s425.kdlfps.com', '18866')

    def process_request(self, request, spider):

        # 用户名密码认证
        username = "f2470416461"
        password = "smueu1d8"
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": ':'.join(ProxyDownloaderMiddleware._proxy)}

        # 白名单认证
        # request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy}

        request.headers["Connection"] = "close"
        return None

    def process_exception(self, request, exception, spider):
        """捕获407异常"""
        if "'status': 407" in exception.__str__():  # 不同版本的exception的写法可能不一样，可以debug出当前版本的exception再修改条件
            from scrapy.resolver import dnscache
            dnscache.__delitem__(ProxyDownloaderMiddleware._proxy[0])  # 删除proxy host的dns缓存
        return exception

class CloudScraperMiddleware:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()  # 创建 CloudScraper 实例

    def process_request(self, request, spider):
        # 使用 CloudScraper 发送请求
        response = self.scraper.get(request.url, headers=request.headers.to_unicode_dict())
        return HtmlResponse(
            url=request.url,
            body=response.content,
            encoding='utf-8',
            request=request
        )

class RandomUserAgentMiddleware:
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.ua.random

class DelayMiddleware:
    def __init__(self, delay_range=(1, 5)):
        self.delay_range = delay_range

    def process_request(self, request, spider):
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)

class FusiondataSpiderMiddleware:
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


class FusiondataDownloaderMiddleware:
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
