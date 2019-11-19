# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from pinera.items import DownloadItem


class ScrapperSpider(scrapy.Spider):
    name = 'scrapper'
    # allowed_domains = ['presidencia.cl/']
    start_urls = ['http://prensa.presidencia.cl/discursos.aspx/']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    }

    def parse(self, response):     
        PAGE_SELECTOR = "//a[contains(@class,'btn')]/@href"
        prefix = 'https://prensa.presidencia.cl/' #because urljoin method is not working properly
        for page in response.xpath(PAGE_SELECTOR).extract():
            yield scrapy.Request(prefix+'/'+page, callback=self.parseDiscurso)
        
        for next_link in response.xpath("(//a[contains(@class,'next')]/@href)[1]").extract():
            yield scrapy.Request(prefix+next_link, callback=self.parse)

    
    def parseDiscurso(self, response):
        LINK_SELECTOR = "//a[contains(@class,'btn-descargar')]/@href"
        print(response.xpath(LINK_SELECTOR))
        for link in response.xpath(LINK_SELECTOR): 
            loader = ItemLoader(item=DownloadItem())
            rel_link = link.extract()
            prefix = 'https://prensa.presidencia.cl/' #because urljoin method is not working properly
            full_link = prefix+rel_link
            loader.add_value('file_urls', full_link)
            loader.add_value('files', rel_link)
            loader.add_value('file_name', rel_link)
            yield loader.load_item()

