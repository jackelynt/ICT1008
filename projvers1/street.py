# -*- coding: utf-8 -*-
# Street names from: https://geographic.org/streetview/singapore/index.html
import scrapy

class StreetSpider(scrapy.Spider):
    name = 'street'
    allowed_domains = ['geographic.org']
    start_urls = ['http://geographic.org/streetview/singapore/index.html/']

    def parse(self, response):
            for name in response.css(".listspan"):
                yield
                {
                    "streetname":  name.css('alt="([^"]*)').extract_first()
                }
