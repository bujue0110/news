import datetime
import scrapy


from news.items import NewsItem


class NewsSpider(scrapy.spiders.Spider):
    name = "news"
    #allowed_domains = ["yidaiyilu.gov.cn/"]
    # start_urls = [
    #     "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10002",
    #     "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10005",
    #     "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10003",
    #     "https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10004"
    # ]
    start_urls = [
        "https://www.yidaiyilu.gov.cn/"
    ]


    def parse(self, response):
        #news list
        # for sel in response.xpath("//div[@class='left_content left']/a/@href"):
        #     if(sel):
        #         url = 'https://www.yidaiyilu.gov.cn%s' % sel.extract()
        #         yield scrapy.Request(url, callback=self.parse)
        #scroll news
        for sel in response.xpath("//div[@class='bd']/ul/li/a/@href"):
            if (sel):
                url = 'https://www.yidaiyilu.gov.cn%s' % sel.extract()
                yield scrapy.Request(url, callback=self.parse)
        item = NewsItem()
       #print response.body
        item['time'] = response.xpath("//div[@class='szty']/span[1]/text()").extract()
        #item['time'] = datetime.datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
        item['url']= response.url
        item['title'] = response.xpath('//title/text()').extract()[0][:-10]
        item['content'] = response.xpath("//p[@style='text-indent:2em;']/text()").extract()
        item['img_url'] = response.xpath("//div[@class='info_content']/p/img/@src").extract()
        item['source'] = response.xpath("//div[@class='szty']/span[2]/text()").extract()
        item['type'] = response.xpath("//ul[@class='local_ul']/li[5]/a/text()").extract()
        item['desc'] = response.xpath("//meta[@name='description']/@content").extract()
        yield item


