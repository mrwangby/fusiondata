import scrapy


class SciencedirectSpider(scrapy.Spider):
    name = "sciencedirect"
    allowed_domains = ["sciencedirect.com"]
    start_urls = ["https://www.sciencedirect.com"]

    def parse(self, response):
        # 打印请求头信息
        print("请求头：", response.request.headers)
        # 或者查看单个请求头
        print("User-Agent：", response.request.headers.get("User-Agent"))
        print(response.body)
        pass
