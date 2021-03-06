# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib.parse import urlparse

from scrapy.pipelines.files import FilesPipeline
from scrapy import Request

class PineraPipeline(object):
    def process_item(self, item, spider):
        return item

class DownloadPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        file_url = item['file_urls'][0]
        meta = {'filename': item['file_name']}
        yield Request(url=file_url, meta=meta)

    def file_path(self, request, response=None, info=None):
        path = request.meta.get('filename','')[0]
        return path

