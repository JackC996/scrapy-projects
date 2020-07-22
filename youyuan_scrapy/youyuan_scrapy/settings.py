# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html

# 项目爬虫位置 我的项目名为youyuan_spider 所以讲example改为youyuan_spider
SPIDER_MODULES = ['youyuan_scrapy.spiders']
NEWSPIDER_MODULE = 'youyuan_scrapy.spiders'


# 选择去重类 scrapy_redis里的去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 使用了scrapy-redis里的去重组件，不使用scrapy默认调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复，也就是不清理redis queues
SCHEDULER_PERSIST = True

# 默认的 按优先级排序(Scrapy默认)，由sorted set实现的一种非FIFO、LIFO方式
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# 可选的 按先进先出排序（FIFO）
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# 可选的 按后进先出排序（LIFO）
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

# 只在使用SpiderQueue或者SpiderStack是有效的参数，指定爬虫关闭的最大间隔时间
# SCHEDULER_IDLE_BEFORE_CLOSE = 10


# 通过配置RedisPipeline将item写入key为 spider.name : items 的redis的list中，供后面的分布式处理item
# 这个已经由 scrapy-redis 实现，不需要我们写代码
ITEM_PIPELINES = {
    "youyuan_scrapy.pipelines.YouyuanspiderPipeline":100,
    'youyuan_scrapy.pipelines.ExamplePipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

LOG_LEVEL = 'INFO'

# 指定redis数据库的连接参数
# 指定redis数据库的ip
REDIS_HOST = ''
# 指定数据库的端口
REDIS_PORT = 6379

#  设置密码
REDIS_PARAMS = {
    'password': '',
}

SPIDER_MIDDLEWARES = {
   # 'youyuanSpider.middlewares.YouyuanspiderSpiderMiddleware': 543,
   'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,   #使用scrapy-redis分布式时，必须写这个，不然会报错 ：[scrapy.spidermiddlewares.offsite] DEBUG: Filtered offsite request to 'www.youyuan.com'
}


# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
# 下载延迟
# DOWNLOAD_DELAY = 0.5

# CONCURRENT_REQUESTS = 4

# 设置超时时间
DOWNLOAD_TIMEOUT = 3

# 尝试次数
RETRY_TIMES = 20

# 覆盖默认请求头，可以自己编写Downloader Middlewares设置代理和UserAgent
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, sdch'
}

#默认情况下,RFPDupeFilter只记录第一个重复请求。将DUPEFILTER_DEBUG设置为True会记录所有重复的请求。
# DUPEFILTER_DEBUG =True

TELNETCONSOLE_PORT = None
