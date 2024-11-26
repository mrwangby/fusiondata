import scrapy


class AgupubsSpider(scrapy.Spider):
    name = "agupubs"
    allowed_domains = ["agupubs.onlinelibrary.wiley.com"]
    start_urls = ["https://agupubs.onlinelibrary.wiley.com"]

    def parse(self, response):
        # 打印请求头信息
        print("请求头：", response.request.headers)
        # 或者查看单个请求头
        print("User-Agent：", response.request.headers.get("User-Agent"))
        print(response.body)
        pass
