import scrapy
from bs4 import BeautifulSoup
from fusiondata.items import PubsItem 
import os
from scrapy import Request
import time
from scrapy.exceptions import IgnoreRequest
#from scrapy_playwright.page import PageCoroutine

class PubsSpider(scrapy.Spider):
    name = "pubs"
    allowed_domains = ["aip.org"]
    start_urls = ["https://pubs.aip.org/aip/pop/issue"]

    def start_requests(self):
        base_url = "https://pubs.aip.org/aip/pop/issue/{}/{}"
        for volume in range(1, 2):  # 从第1卷到第2卷
            for issue in range(4, 5):  # 从第1期到第12期
                url = base_url.format(volume, issue)
                print(url)
                yield scrapy.Request(url, self.parse)

    def save_pdf(self, response):
        item = response.meta['item']
        valid_filename = "".join(x for x in item['title'] if x.isalnum() or x in "._- ")
        pdf_path = os.path.join('pdfs', f"{valid_filename}.pdf")
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        with open(pdf_path, 'wb') as f:
            f.write(response.body)

        # 更新 item 的 PDF 路径
        item['pdf_path'] = pdf_path
        yield item

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        with open("output.html", "w", encoding='utf-8') as file:
            file.write(soup.prettify())
        base_url = "https://pubs.aip.org"  # 基础链接
        for record in response.xpath("//div[@class='al-article-item-wrap al-normal']"):
            item = PubsItem()
            # 提取标题
            item['title'] = record.xpath(".//h5[@class='customLink item-title']/a/text()").get()
            # 提取作者列表
            item['authors'] = record.xpath(".//div[@class='al-authors-list']//a/text()").getall()
            # 提取期刊信息
            item['journal_info'] = record.xpath(".//div[@class='ww-citation-primary']/em/text()").get()
            # 提取 DOI
            item['doi'] = record.xpath(".//div[@class='ww-citation-primary']//a[@href]/text()").get()
            # 提取摘要链接
            item['abstract_link'] = record.xpath(".//a[contains(@class, 'showAbstractLink')]/@href").get()
            # 提取 PDF 下载链接
            item['pdf_link'] = base_url+record.xpath(".//a[contains(@class, 'article-pdfLink')]/@href").get()
            time.sleep(1)
            print(item)
            print("===================================")
            if item['pdf_link']:
                pdf_url = item['pdf_link'] if item['pdf_link'].startswith('http') else f"https://pubs.aip.org{item['pdf_link']}"
                yield Request(
                    pdf_url,
                    meta={'item': item},
                    callback=self.save_pdf
                )
            else:
                yield item