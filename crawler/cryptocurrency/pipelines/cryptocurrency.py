import json
import logging
import scrapy
from datetime import datetime

logger = logging.getLogger(__name__)


class CryptocurrencySavePipeline:

    def __init__(self, crawler, market: dict, market_save: str, cryptocurrency_save: str, price_save: str):
        self.crawler = crawler
        self.market = market
        self.market_save = market_save
        self.cryptocurrency_save = cryptocurrency_save
        self.price_save = price_save

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            cryptocurrency_save=crawler.settings['CRYPTOCURRENCY_SAVE_URL'],
            market_save=crawler.settings['MARKET_SAVE_URL'],
            price_save=crawler.settings['PRICE_SAVE_URL'],
            crawler=crawler,
            market=crawler.spidercls.market,
        )

    def open_spider(self, spider):
        self.crawler.engine.crawl(
            scrapy.Request(url=self.market_save, method='POST', body=json.dumps(self.market), callback=self.save),
            spider,
        )

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item['marketId'] = self.market['marketId']
        if item.get('contracts'):
            item['contracts'] = [{**i, **{'marketId': self.market['marketId']}} for i in item['contracts']]

        if len(item.keys()) > 2:
            self.crawler.engine.crawl(
                scrapy.Request(url=self.cryptocurrency_save, method='POST', meta={'item': item},
                               body=json.dumps(item, default=self.default_converter), dont_filter=True,
                               callback=self.save
                               ),
                spider,
            )
            return item

    def save(self, response):
        if response.status == 200:
            if response.url == self.market_save:
                logger.info("==================== CREATE NEW MARKET ====================")
            if response.url == self.cryptocurrency_save:
                _price = response.meta['item'].get('price')
                if not _price:
                    logging.warning(response.text)
                    pass
                body = [
                    {**i, **{'marketId': self.market['marketId'], 'cryptocurrencyId': json.loads(response.text)['id']}}
                    for i in _price
                ]
                yield scrapy.Request(
                    url=self.price_save,
                    method='POST',
                    body=json.dumps(body, default=self.default_converter), dont_filter=True, callback=self.save
                )
        else:
            logging.error(response.text)

    @staticmethod
    def default_converter(o):
        if isinstance(o, datetime):
            return o.__str__()
