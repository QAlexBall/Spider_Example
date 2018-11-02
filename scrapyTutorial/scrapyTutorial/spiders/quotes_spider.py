import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    """
    On scrapy 1.5.1
    * name: identifies the Spider.
    * start_requests(): must return an iterable of Requests which the Spider will begin to crawl from.
    * parse(): a method that will be called to handle the response downloader for each of the request made.
    """
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_bak(self, response):
    	page = response.url.split("/")[-2]
    	filename = 'quotes-%s.html' % page
    	with open(filename, 'wb') as f:
    	    f.write(response.body)
    	self.log('Saved file %s' % filename)

    def parse_bak0(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract()
            }

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                    'text': quote.css('span.text::text').extract_first(),
                    'author': quote.css('small.author::text').extract_first(),
                    'tags': quote.css('div.tags a.tag::text').extract()
            }
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

"""
To put our spider to work, go to project's top level directory and run:
    scrapy crawl quotes
This command runs the spider with name quotes that we've just added.
that will send some requests for the quotes.toscrape.com domain.
"""

"""
'''
A shortcut to start_requests method

The parse() method will be called to handle each of requests for thos URLs,
even though we haven't explicitly told Scrapy to do so.
'''
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
    	'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/'
    ]

    def parse_bak(self, response):
        page = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract()
            }
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
"""
