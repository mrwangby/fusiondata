import scrapy


class LinkSpider(scrapy.Spider):
    name = "link"
    allowed_domains = ["springer.com"]
    start_urls = ["https://link.springer.com"]

    def parse(self, response):
        pass
