import scrapy
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urljoin
from scrapy import Request
from fusiondata.items import iaeaItem
from fake_useragent import UserAgent
from scrapy.resolver import dnscache
from urllib.parse import quote
import os

class InisSpider(scrapy.Spider):
    name = "inis"
    allowed_domains = ["inis.iaea.org"]
    def __init__(self, *args, **kwargs):
        super(InisSpider, self).__init__(*args, **kwargs)
        self.search_terms = ["non-linear effects in plasma", "non-linear wave-particle resonant effect",
"three-wave process", "plasma echo", "parametric excitation (parametric instability)",
"side-band effect", "non-linear wave", "laser light scattering by plasma",
"stimulated Raman scattering", "Stimulated Brillouin scattering",
"modulational instability", "envelope instability", "decay instability",
"plasma turbulence", "plasma magnetohydrodynamic turbulence", "weak turbulence",
"strong turbulence", "quasi-linear theory", "soliton"]
        '''self.search_terms = [
            "Neutral Beam Injection System Design","Radio Frequency Heating Systems","Electron Cyclotron Heating","Ion Cyclotron Heating","Lower Hybrid Current Drive Systems","Antenna and Waveguide Design","High-Power Microwave Technology","ECH","ICH",
            "Magnetic Diagnostic Equipment","Laser Interferometry Systems","Thomson Scattering Diagnostics","Neutron Diagnostic Techniques","X-ray Imaging Systems","Spectroscopic Diagnostics","Data Processing and Analysis Software",
        ]'''
        self.download_pdf = True  # 启用 PDF 下载功能
    

    def save_pdf(self, response):
        # 从 meta 获取 item 和 search_term
        item = response.meta['item']
        search_term = item['search_term']
        
        # 创建以 search_term 命名的子文件夹路径
        search_term_folder = os.path.join('pdfs', search_term)
        os.makedirs(search_term_folder, exist_ok=True)
        
        # 确保文件名有效
        valid_filename = "".join(x for x in item['title'] if x.isalnum() or x in "._- ")
        pdf_path = os.path.join(search_term_folder, f"{valid_filename}.pdf")

        # 保存 PDF 文件
        with open(pdf_path, 'wb') as f:
            f.write(response.body)
        
        
        # 返回 item
        yield item

    def start_requests(self):
            base_url = 'https://inis.iaea.org/search/search.aspx?search-option=everywhere&orig_q='
            for term in self.search_terms:
                # 关键字编码为 URL 格式
                encoded_term = quote(f'fusion AND "{term}"')
                url = f'{base_url}{encoded_term}&mode=Advanced&fulltext=true&translateTo='
                print(term+"开始爬取"+url)
                self.logger.info(term+"开始爬取") 
                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'search_term': term})
    def parse(self, response, search_term):
        # Extract necessary data
        for record in response.xpath("//div[@class='result-default-view']"):
            pdf_link = record.xpath(".//a[contains(@class, 'fileTypeIcon')]/@href").get()
            pdf_link_full = urljoin(response.url, pdf_link) if pdf_link else None
            title = record.xpath(".//div[@class='g1-title']//span[@class='englishtitle title']/text()").get()
            if not title:
                continue  # Skip records without titles
            author = record.xpath(".//div[@class='g1-metadata']//span[@class='aut-cc author']/a/text()").getall()
            author = ', '.join(author) if author else None
            year = record.xpath(".//div[@class='g1-metadata']//small[@class='text-muted d-block year']/text()").get()
            abstract = record.xpath(".//div[@class='g1-metadata']//span[@class='lead-cc leadtitle title']/text()").get()
            primary_subject = record.xpath(".//div[@class='metadata-row']//div[@class='primarysubject subject']/a/text()").get()
            item = {
                'title': title,
                'link': response.urljoin(record.xpath(".//a[contains(@class, 'title-link')]/@href").get()),
                'author': author,
                'year': year,
                'abstract': abstract,
                'primary_subject': primary_subject,
                'pdf_url': pdf_link_full,
                'search_term': search_term,
            }

            

            # 处理 PDF 链接
#            if item['pdf_url']:
#                pdf_url = item['pdf_url']
#                yield Request(
#                    pdf_url,
#                    meta={'item': item},
#                    callback=self.save_pdf
#                )
#            else:
#                yield item
            yield item

        # Handle pagination links
        next_page = response.xpath("//a[@ctype='nav.next']/@href").get()
        if next_page:
            next_page_full = urljoin(response.url, next_page)
            print("下一页"+next_page_full)
            yield scrapy.Request(url=next_page_full, callback=self.parse, cb_kwargs={'search_term': search_term})
        else:
            print(search_term+"爬取完了")
            self.logger.info(search_term+"爬取完了") 
