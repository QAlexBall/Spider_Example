# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
"""
Item是保存爬取到的数据的容器,其使用方法和python的字典类似
首先根据需要从dmoz.org获取的数据对item进行建模
"""
class BaiduItem(scrapy.Item):
	title = scrapy.Field()
	link = scrapy.Field()
	desc = scrapy.Field()

class ScrapytutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
