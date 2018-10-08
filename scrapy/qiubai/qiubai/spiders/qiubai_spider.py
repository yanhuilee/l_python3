# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector.unified import SelectorList
from qiubai.item import QiubaiItem

class QiuBaiSpider(scrapy.Spider):
    name = 'qiubai'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1']

    def parse(self, response):
        # SelectorList
        contentLeftDiv = response.xpath("//div[@id='content-left']/div")

        print("="*40)
        for contentDiv in contentLeftDiv:
            #  <Selector xpath="//div[@id='content-left']/div" data='<div class="article block untagged mb15 '>
            author = contentDiv.xpath(".//h2/text()").get().strip()
            print("author: ", contentDiv.xpath(".//h2/text()").get().strip())
            content = contentDiv.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()
            print("content: ", content)

            duanzi = {'author': author, 'content': content}
            yield duanzi