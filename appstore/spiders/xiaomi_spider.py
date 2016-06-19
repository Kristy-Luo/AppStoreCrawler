import scrapy
import re
from scrapy.selector import Selector
from appstore.items import AppstoreItem


class XiaomiSpider(scrapy.Spider):
    name = "xiaomi"
    allowed_domains = ["app.mi.com"]

    start_urls = ["http://app.mi.com/topList?page=1"]

    def parse(self, response):
        page = Selector(response)

        divs = page.xpath('//ul[@class="applist"]/li')

        for div in divs:
            item = AppstoreItem()
            item['title'] = div.xpath('./h5/a/text()').extract_first().encode('utf-8')
            item['url'] = div.xpath('./h5/a/@href').extract_first()
            appid = re.match(r'/detail/(.*)', item['url']).group(1)
            item['appid'] = appid
            item['intro'] = div.xpath('.//p[@class="app-desc"]/a/text()'). \
                extract_first().encode('utf-8')
            yield item