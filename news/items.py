# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    img_url = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    pass
