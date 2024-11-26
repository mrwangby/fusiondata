import scrapy
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urljoin
import os
from fusiondata.items import iaeaItem
from fake_useragent import UserAgent
from scrapy.resolver import dnscache
from urllib.parse import quote
import json
class InisSpider(scrapy.Spider):
    name = "num"
    allowed_domains = ["inis.iaea.org"]
    def __init__(self, *args, **kwargs):
        super(InisSpider, self).__init__(*args, **kwargs)
        self.search_terms =      ["waves in plasma", "dispersion relation", "Clemmow-Mullaly-Allis diagram", 
 "wave energy", "positive energy wave", "negative energy wave", "longitudinal wave", 
 "electrostatic wave", "electron plasma oscillation", "Langmuir wave", "ion wave", 
 "ion plasma oscillation", "ion plasma wave", "ion sound speed", "magnetosonic waves", 
 "magnetosonic velocity", "Alfven wave", "Alfven velocity", 
 "magnetohydrodynamic wave", "slow magnetosonic wave", "ion-sound wave", 
 "oblique Alfven wave", "fast magnetosonic wave", 
 "Appleton-Hartree dispersion relation", "ion cyclotron wave", "whistler wave", 
 "helicon wave", "electron cyclotron wave", "ordinary wave", "extraordinary wave", 
 "lower hybrid wave", "lower hybrid frequency", "upper hybrid wave", 
 "upper hybrid frequency", "Bernstein wave", "drift waves", "BGK mode", 
 "pseudowavefront", "deflagration wave", "combustion wave"]
        self.download_pdf = True  # 启用 PDF 下载功能

        '''    def start_requests(self):
        base_url = 'https://inis.iaea.org/search/search.aspx?search-option=everywhere&orig_q='
        for term in self.search_terms:
            encoded_term = quote(f'"{term}"')
            url = f'{base_url}{encoded_term}&mode=Advanced&fulltext=true&translateTo='
            print(url)
            print("-------------------------")
            yield scrapy.Request(url=url, callback=self.parse,cb_kwargs={'search_term': term})'''
    
    def start_requests(self):
        base_url = 'https://inis.iaea.org/search/search.aspx?search-option=everywhere&orig_q='
        for term in self.search_terms:
            # 关键字编码为 URL 格式
            encoded_term = quote(f'fusion AND "{term}"')
            url = f'{base_url}{encoded_term}&mode=Advanced&fulltext=true&translateTo='
            print(url)
            print("-------------------------")
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'search_term': term})

    def parse(self, response,search_term):

        # 提取第三个<b>标签内容（0.054）
        third_b = response.xpath('//div[@class="col-lg-8 d-none d-lg-block"]/b[3]/text()').get()



        print(search_term)
        print(third_b)
        data = {
        "search_term": search_term,
        "num": third_b
    }

    # 定义要保存的文件路径
        file_path = 'output_data.json'

        # 读取现有的 JSON 文件内容（如果文件已存在）
        try:
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        # 将新数据添加到现有数据列表中
        existing_data.append(data)

        # 将更新后的数据写回到 JSON 文件
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)


