import scrapy


class QuotesSpider(scrapy.Spider):
    # 定义爬虫名称
    name = "quotes"

    def start_requests(self):
        # 爬取地址
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        file_name = 'quotes-{page}.html'.format(page=page)
        with open(file_name, 'wb') as file:
            file.write(response.body)
        self.log('Saved file {file_name}'.format(file_name=file_name))


from scrapy.crawler import CrawlerProcess
# 导入获取项目设置信息
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('quotes')
    process.start()