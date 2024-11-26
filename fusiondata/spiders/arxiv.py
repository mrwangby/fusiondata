import scrapy


class ArxivSpider(scrapy.Spider):
    name = "arxiv"
    allowed_domains = ["arxiv.org"]
    start_urls = ["https://arxiv.org"]

    def parse(self, response):
        pass
