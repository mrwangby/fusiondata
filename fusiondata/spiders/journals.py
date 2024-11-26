import scrapy


class JournalsSpider(scrapy.Spider):
    name = "journals"
    allowed_domains = ["aps.org"]
    start_urls = ["https://journals.aps.org"]

    def parse(self, response):
        pass
