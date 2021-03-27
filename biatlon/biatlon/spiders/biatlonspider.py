import scrapy


class BiatlonspiderSpider(scrapy.Spider):
    name = 'biatlonspider'
    allowed_domains = ['biatlon.com']
    start_urls = ['http://biatlon.com/']

    def parse(self, response):
        pass
