import datetime
import scrapy


from news.items import NewsItem


class NewsSpider(scrapy.spiders.Spider):
    name = "news"
    #allowed_domains = ["yidaiyilu.gov.cn/"]
    start_urls = [
        "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10005"
    ]

    # def start_requests(self):
    #     url = "https://www.yidaiyilu.gov.cn/xwzx/hwxw/41021.htm"
    #     return scrapy.Request(url, callback=self.parse)
    def parse(self, response):
        for sel in response.xpath("//div[@class='left_content left']/a/@href"):
            if(sel):
                url = 'https://www.yidaiyilu.gov.cn%s' % sel.extract()
                yield scrapy.Request(url, callback=self.parse)
        item = NewsItem()
       #print response.body
        item['time'] = response.xpath("//span[@class='main_content_date szty1 '][1]/text()").extract()
        item['url']= response.url
        item['title'] = response.xpath('//title/text()').extract()[0][:-10]
        item['desc'] = response.xpath("//p[@style='text-indent:2em;']/text()").extract()
        item['img_url'] = response.xpath("//div[@class='info_content']/p/img/@src").extract()
        item['source'] = response.xpath("//span[@class='main_content_date szty2']/text()").extract()
        item['type'] = response.xpath("//ul[@class='local_ul']/li[5]/a/text()").extract()
        yield item


