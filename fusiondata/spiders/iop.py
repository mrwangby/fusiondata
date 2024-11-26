import scrapy
from bs4 import BeautifulSoup
from fusiondata.items import iopItem 
from urllib.parse import urljoin 
import requests
import time
from scrapy import Request
class IopSpider(scrapy.Spider):

    name = "iop"
    #allowed_domains = ["iop.org"]
    start_urls = ["https://iopscience.iop.org/issue/1009-0630/21/3"]
    def start_requests(self):
        url = "https://iopscience.iop.org/issue/1009-0630/21/3"
        yield scrapy.Request(url, self.parse)
    def nn(self, response):
        print(f"Proxy used: {response.meta.get('proxy', 'No proxy')}")
        print(response.text)
    def parse(self, response):
            soup = BeautifulSoup(response.text, 'html.parser')
            with open("iop.html", "w", encoding='utf-8') as file:
                file.write(soup.prettify())
            base_url = "https://iopscience.iop.org/" # 基础链接
            for record in response.xpath("//div[@class='art-list-item reveal-container reveal-closed']"):
                #print(record.get())
                print("===================================")
                paper_id = record.xpath(".//div[@class='indexer']/text()").get()

                # 提取论文标题
                title = record.xpath(".//a[@class='art-list-item-title']/text()").get().strip()

                # 提取作者信息
                authors = record.xpath(".//p[@class='small art-list-item-meta']//span[@itemprop='name']/text()").getall()
                authors = ", ".join(authors)  # 合并为逗号分隔的字符串

                # 提取摘要（隐藏内容）
                abstract = record.xpath(".//div[@class='reveal-content']//p/text()").get(default="").strip()

                # 提取 DOI 链接
                doi_link = record.xpath(".//div[@class='reveal-content']//a[contains(@href, 'doi')]/@href").get()

                # 提取文章链接
                article_link = record.xpath(".//a[contains(@href, 'meta')]/@href").get()

                # 提取 PDF 链接
                pdf_link = record.xpath(".//a[contains(@href, 'pdf')]/@href").get()

                # 组合完整链接（如果需要）
                if article_link:
                    article_link = base_url + article_link
                if pdf_link and not pdf_link.startswith("http"):
                    pdf_link = base_url + pdf_link
                if doi_link and not doi_link.startswith("http"):
                    doi_link = base_url + doi_link
                time
                # 返回爬取结果
                yield {
                    'paper_id': paper_id,
                    'title': title,
                    'authors': authors,
                    'abstract': abstract,
                    'doi_link': doi_link,
                    'article_link': article_link,
                    'pdf_link': pdf_link,
                    'cat': 'IOP'
                }       
            next_page = response.xpath('//a[@class="ml-1"]/@href').get()
            if next_page:
                ll = "https://dev.kdlapi.com/testproxy"
                yield scrapy.Request(ll, callback=self.nn)
                next_page_full = urljoin(base_url, next_page)
                print("Next page: ", next_page_full)
                yield scrapy.Request(url=next_page_full, callback=self.parse)