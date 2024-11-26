# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FusiondataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PubsItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()
    journal_info = scrapy.Field()
    doi = scrapy.Field()
    abstract_link = scrapy.Field()
    pdf_link = scrapy.Field()

class iaeaItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    year = scrapy.Field()
    abstract = scrapy.Field()
    primary_subject = scrapy.Field()
    pdf_url = scrapy.Field()
    search_term = scrapy.Field()

class iopItem(scrapy.Item):
    # 论文编号
    paper_id = scrapy.Field()
    # 论文标题
    title = scrapy.Field()
    # 作者信息
    authors = scrapy.Field()
    # 摘要
    abstract = scrapy.Field()
    # DOI 链接
    doi_link = scrapy.Field()
    # 文章链接
    article_link = scrapy.Field()
    # PDF 下载链接
    pdf_link = scrapy.Field()
    # 期刊信息
    cat = scrapy.Field()

