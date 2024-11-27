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
    link = scrapy.Field()  # The link to the PDF or main page
    author = scrapy.Field()
    year = scrapy.Field()
    abstract = scrapy.Field()
    primary_subject = scrapy.Field()
    pdf_url = scrapy.Field()  # Full link to the PDF file
    search_term = scrapy.Field()  # The search term used
    source = scrapy.Field()  # The source of the document
    record_type = scrapy.Field()  # Type of the record (e.g., report, article)
    report_number = scrapy.Field()  # Report identification number
    country = scrapy.Field()  # Country associated with the report
    descriptors_dei = scrapy.Field()  # DEI descriptors for classification
    descriptors_dec = scrapy.Field()  # DEC descriptors for classification
    reference_number = scrapy.Field()  # Reference number of the document
    inis_volume = scrapy.Field()  # INIS volume number
    inis_issue = scrapy.Field()  # INIS issue number

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

