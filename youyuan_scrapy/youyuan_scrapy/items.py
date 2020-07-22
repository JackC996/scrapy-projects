# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()

class youyuanItem(Item):
    # 个人头像链接
    header_url = Field()
    # 用户名
    username = Field()
    # 内心独白
    monologue = Field()
    # 相册图片链接
    pic_urls = Field()
    # 年龄
    age = Field()

    # 网站来源 youyuan
    source = Field()
    # 个人主页源url
    source_url = Field()

    # 获取UTC时间
    crawled = Field()
    # 爬虫名
    spider = Field()


class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
