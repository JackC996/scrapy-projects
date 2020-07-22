from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from youyuan_scrapy.items  import youyuanItem
from scrapy_redis.spiders import RedisCrawlSpider
import re

class YouyuanCrawler(RedisCrawlSpider):

    # 修改父类
    name = 'youyuan_redis'
    # 统一管理指令
    redis_key = 'youyuan:start_urls'


    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(YouyuanCrawler, self).__init__(*args, **kwargs)

        # 主页

    page_links = LinkExtractor(allow=r"/mm18-0/advance-0-0-0-0-0-0-0/p\d+/")
    # 详情页面
    profile_page_lx = LinkExtractor(allow=(r'/\d+-profile/'))
    rules = (
        Rule(page_links, follow=True),
        # 匹配个人主页的链接，形成request保存到redis中等待调度，一旦有响应则调用parse_profile_page()回调函数处理，不做继续跟进
        Rule(profile_page_lx, callback='parse_profile_page'),
    )


     # 处理个人主页信息，得到我们要的数据
    def parse_profile_page(self, response):
            item = youyuanItem()
            item['header_url'] = self.get_header_url(response)
            item['username'] = self.get_username(response)
            item['monologue'] = self.get_monologue(response)
            item['pic_urls'] = self.get_pic_urls(response)
            item['age'] = self.get_age(response)
            item['source'] = 'youyuan'
            item['source_url'] = response.url
            print(item)

            # print "Processed profile %s" % response.url
            yield item

        # 提取头像地址
    def get_header_url(self, response):
            header = response.xpath('//dl[@class=\'personal_cen\']/dt/img/@src').extract()
            if len(header) > 0:
                header_url = header[0]
            else:
                header_url = ""
            return header_url.strip()

        # 提取用户名
    def get_username(self, response):
            usernames = response.xpath("//dl[@class=\'personal_cen\']/dd/div/strong/text()").extract()
            if len(usernames) > 0:
                username = usernames[0]
            else:
                username = "NULL"
            return username.strip()

        # 提取内心独白
    def get_monologue(self, response):
            monologues = response.xpath("//ul[@class=\'requre\']/li/p/text()").extract()
            if len(monologues) > 0:
                monologue = monologues[0]
            else:
                monologue = "NULL"
            return monologue.strip()

        # 提取相册图片地址
    def get_pic_urls(self, response):
            pic_urls = []
            data_url_full = response.xpath('//li[@class=\'smallPhoto\']/@data_url_full').extract()
            if len(data_url_full) <= 1:
                pic_urls.append("");
            else:
                for pic_url in data_url_full:
                    pic_urls.append(pic_url)
            if len(pic_urls) <= 1:
                return "NULL"
            # 每个url用|分隔
            return '|'.join(pic_urls)

        # 提取年龄
    def get_age(self, response):
            age_urls = response.xpath("//dl[@class=\'personal_cen\']/dd/p[@class=\'local\']/text()").extract()
            if len(age_urls) > 0:
                age = age_urls[0]
            else:
                age = "0"
            age_words = re.split(' ', age)
            if len(age_words) <= 2:
                return "0"
            age = age_words[2][:-1]
            # 从age字符串开始匹配数字，失败返回None
            if re.compile(r'[0-9]').match(age):
                return age
            return "0"
