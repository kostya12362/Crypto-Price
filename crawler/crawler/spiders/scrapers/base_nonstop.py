import time
import scrapy
import scrapy.signals as sgn


class BaseNonStopSpider(scrapy.Spider):
    TIME_SLEEP = 70
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'ITEM_PIPELINES': {
            'crawler.spiders.pipelines.price.PriceSavePipeline': 120
        }
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        from_crawler = super().from_crawler
        spider = from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.idle, signal=sgn.spider_idle)
        return spider

    def idle(self):
        self.crawler.engine.crawl(scrapy.Request('https://www.google.com/',
                                                 callback=self.clean_buffer,
                                                 dont_filter=True),
                                  self)
        time.sleep(self.TIME_SLEEP)
        for url in self.start_urls:
            req = scrapy.Request(url, callback=self.parse, dont_filter=True)
            self.crawler.engine.crawl(req, self)

    def clean_buffer(self, response):
        yield
