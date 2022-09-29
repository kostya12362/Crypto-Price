import json
import logging
import scrapy
from datetime import datetime
from .base import BasePipeline


class ContractsListSavePipeline(BasePipeline):

    def __init__(self, crawler, map_lists: list, market_save: str, contract_save: str):
        self.crawler = crawler
        self.map_lists = map_lists
        self.market_save = market_save
        self.contract_save = contract_save

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            market_save=crawler.settings['MARKET_SAVE_URL'],
            contract_save=crawler.settings['CONTRACT_SAVE_URL'],
            crawler=crawler,
            map_lists=crawler.spidercls.MAP_LISTS,
        )

    def open_spider(self, spider):
        for market in self.map_lists:
            self.crawler.engine.crawl(
                scrapy.Request(url=self.market_save, method='POST', body=json.dumps(market), callback=self.save),
                spider,
            )

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # item['marketId'] = self.market['id']
        # if item.get('contracts'):
        #     item['contracts'] = [{**i, **{'marketId': self.market['id']}} for i in item['contracts']]

        # if len(item.keys()) > 2:
        #     self.crawler.engine.crawl(
        #         scrapy.Request(url=self.cryptocurrency_save, method='POST', meta={'item': item},
        #                        body=json.dumps(item, default=self.default_converter), dont_filter=True,
        #                        callback=self.save
        #                        ),
        #         spider,
        #     )
        # else:
        # for contract in item['contracts']:
        self.crawler.engine.crawl(
            scrapy.Request(url=self.contract_save, method='POST', meta={'item': item},
                           body=json.dumps(item, default=self.default_converter), dont_filter=True,
                           callback=self.save
                           ),
            spider,
        )

        return item

    def save(self, response):
        if response.status == 200:
            if response.url == self.market_save:
                logging.info("==================== CREATE NEW MARKET ====================")
        else:
            logging.error(response.text)

    @staticmethod
    def default_converter(o):
        if isinstance(o, datetime):
            return o.__str__()
