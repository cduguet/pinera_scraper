# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
import os

class PineraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# def remove_extension(value):
#     return os.path.splitext(value)[0]

class DownloadItem(scrapy.Item):
    name = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_name = scrapy.Field()