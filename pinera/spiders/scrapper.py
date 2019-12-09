# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from pinera.items import DownloadItem
import os

class ScrapperSpider(scrapy.Spider):
    name = 'scrapper'
    # allowed_domains = ['presidencia.cl/']
    start_urls = ['http://prensa.presidencia.cl/discursos.aspx']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    }

    def parse(self, response):
        PAGE_SELECTOR = "//a[contains(@class,'btn')]/@href"

        for page in response.xpath(PAGE_SELECTOR).extract():
            yield scrapy.Request(response.urljoin(page), callback=self.parseDiscurso)
        
        for next_link in response.xpath("(//a[contains(@class,'next')][contains(text(),'>')]/@href)").extract():
            yield scrapy.Request(response.urljoin(next_link), callback=self.parse)

    def parseDiscurso(self, response):
        LINK_SELECTOR = "//a[contains(@class,'btn-descargar')]/@href"
        download_links = response.xpath(LINK_SELECTOR).extract()
        if len(download_links) > 0:
            common_name = os.path.splitext(os.path.basename(download_links[0]))[0]
            year = download_links[0].split('/')[3]
        for rel_link in download_links: 
            loader = ItemLoader(item=DownloadItem())
            full_link = response.urljoin(rel_link)
            loader.add_value('file_urls', full_link)
            loader.add_value('files', rel_link)
            extension = os.path.splitext(rel_link)[1]
            file_name = year + "/" + common_name + extension
            loader.add_value('file_name', file_name)
            yield loader.load_item()

