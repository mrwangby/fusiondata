
from fake_useragent import UserAgent
import random

BOT_NAME = "fusiondata"

SPIDER_MODULES = ["fusiondata.spiders"]
NEWSPIDER_MODULE = "fusiondata.spiders"


# 启用自定义的中间件：禁用默认的 UserAgentMiddleware，并启用自定义的 RandomUserAgentMiddleware
DOWNLOADER_MIDDLEWARES = {
    'fusiondata.middlewares.RandomUserAgentMiddleware': 400,  # 启用自定义的 User-Agent 中间件
    #'fusiondata.middlewares.LogRequestHeadersMiddleware': 543,  # 启用自定义的请求头中间件
    #'fusiondata.middlewares.ProxyDownloaderMiddleware': None,
     #'fusiondata.middlewares.ResponseFilterMiddleware': 500,

}
# 启用重试机制
RETRY_ENABLED = True  # 启用自动重试机制
RETRY_TIMES = 5  # 设置最大重试次数为 5 次
RETRY_DELAY = 3  # 设置每次重试之间的延迟为 3 秒
RETRY_HTTP_CODES = [403, 404, 408, 500, 502, 503, 504]  # 指定需要重试的 HTTP 状态码

# 启用自动调整延迟
AUTOTHROTTLE_ENABLED = True  # 启用自动限速
AUTOTHROTTLE_START_DELAY = 2  # 初始延迟2秒
AUTOTHROTTLE_MAX_DELAY = 10   # 最大延迟10秒
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # 每个服务器并发请求数为1
AUTOTHROTTLE_DEBUG = False  # 不启用调试模式

# 设置下载延迟，避免过于频繁的请求
DOWNLOAD_DELAY = 2 # 每个请求之间的间隔时间（秒）
CONCURRENT_REQUESTS = 4               # 全局最大并发请求数
CONCURRENT_REQUESTS_PER_DOMAIN = 2    # 每个域名的最大并发请求数
CONCURRENT_REQUESTS_PER_IP = 2        # 每个IP的最大并发请求数

# 忽略 robots.txt 规则
ROBOTSTXT_OBEY = False

# 禁用 cookies
COOKIES_ENABLED = False  # 禁用 cookies

# 配置 Item Pipeline，用于处理爬取到的数据
ITEM_PIPELINES = {
    "fusiondata.pipelines.FusiondataPipeline": 300,  # 添加 ArxivPipeline 处理管道，优先级为 300
}

# 设置请求指纹生成器的实现
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"  # 使用 Scrapy 默认的请求指纹生成实现


# 设置异步 I/O reactor 为 AsyncioSelectorReactor
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# 设置导出文件的编码格式
FEED_EXPORT_ENCODING = "utf-8"  # 导出文件编码设置为 UTF-8

# 日志配置
LOG_LEVEL = 'DEBUG'  # 设置日志级别为 DEBUG
LOG_FILE = 'scrapy_log.txt'  # 将日志输出到指定文件中

# 启用去重过滤器的调试信息，帮助跟踪请求是否被去重
DUPEFILTER_DEBUG = False  # 启用去重调试信息

DOWNLOADER_CLIENT_TLS_VERIFY = False
DOWNLOADER_CLIENT_TLS_METHOD = "TLSv1.2"


