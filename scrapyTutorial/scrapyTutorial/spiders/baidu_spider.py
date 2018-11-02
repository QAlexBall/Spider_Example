"""
为了创建一个Spider,必须集成scrapy.Spider类,且定义一些属性
name: 用于区别Spider
start_urls: 包含了Spider在启动时进行爬取的url列表
parse(): 是spider的一个方法
"""
import scrapy
from scrapyTutorial.items import BaiduItem
class BaiduSpider(scrapy.Spider):
	name = "baidu"
	allowed_domains = ["baidu.com"]
	start_urls = [
			"https://baike.baidu.com/item/Python/407313",
			"https://baike.baidu.com/item/Java/85979"
    ]
	
	def parse_bak(self, response):
		filename = response.url.split("/")[-2] + '.html'
		with open(filename, 'wb') as f:
			f.write(response.body)

	"""
	Selectors选择器简介
	Selector有四个基本的方法
	xpath()   : 传入xpath表达式,返回该表达式所对应的所有节点的selector list列表
	css()     : 传入CSS表达式,返回该表达式对应所对应的所有节点的selector list列表
	extract() : 序列化该节点为unicode字符串病返回list
	re()	  : 根据传入的正则表达式对数据进行提取,返回unicode字符串list列表
	"""
	def parse_bak1(self, response):
		# 提取数据
		for sel in response.xpath('//ul/li'):
			title = sel.xpath('a/text()').extract()
			link = sel.xpath('a/@href').extract()
			desc = sel.xpath('text()').extract()
			print(title, link, desc)

	"""
	使用Item
	Item对象时自定义的python字典.可以使用标准的字典语法来获取到其每个字段的值.
	>>> item = BaiduItem()
	>>> item['title'] = 'Example title'
	>>> item['title']
	'Example title'
	"""
	def parse(self, response):
		for sel in response.xpath('//ul/li'):
			item = BaiduItem()
			item['title'] = sel.xpath('a/text()').extract()
			item['link'] = sel.xpath('a/@href').extract()
			item['desc'] = sel.xpath('text()').extract()
			yield item

	"""
	...
	...
	...
	{'desc': ['\n', '\n', '\n', '\n'],
 	 'link': ['http://www.baidu.com/p/nde54440?from=wk',
          'https://baike.baidu.com/kedou'],
 	 'title': ['nde54440', '\n', '\n']}
 	 ...
 	 ...
 	 ...
 	"""

"""
进入项目根目录,执行下列命令启动spider
scrapy crawl baidu
查看当前目录,有Java.html和Python.html
Scrapy为Spider的start_urls属性中的每个URL创建了scrapy.Request对象,
并将parse方法作为回调函数(callback)赋值给了Request.

Request对象经过调度,执行生成scrapy.http.Response对象并送回给spider parse()方法
"""