import scrapy
from scrapy import item
from crawl.items import CrawlItem
from scrapy_splash import SplashRequest


class InterestSpider(scrapy.Spider):
    name = "interest"

    def start_requests(self):
        urls = [
            "https://portal.vietcombank.com.vn/Personal/lai-suat/Pages/lai-suat.aspx?devicechannel=default",
        ]
        for url in urls:
            yield scrapy.Request(
                url,
                self.parse,
                meta={"splash": {"endpoint": "render.html", "args": {"wait": 0.5}}},
            )

    def parse(self, response):

        for data in response.xpath("//table//tr"):
            th = data.xpath("./th/text()").get()
            td = data.xpath("./td/text()").get()
            item = CrawlItem()
            if th is not None:
                item["data"] = [x.strip() for x in data.xpath("./th/text()").getall()]
            elif td is not None:
                item["data"] = [x.strip() for x in data.xpath("./td/text()").getall()]
            yield item
