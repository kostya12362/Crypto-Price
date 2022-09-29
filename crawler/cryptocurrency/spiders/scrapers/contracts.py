import json

import scrapy

from ..parsers import ListContractsParser
from .base import BaseSpider


class CoinmarketcapSpider(BaseSpider):
    name = 'contracts'
    handle_httpstatus_list = [422, 500]
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'ITEM_PIPELINES': {
            'cryptocurrency.pipelines.contracts_list.ContractsListSavePipeline': 300
        }
    }
    parser_contract = ListContractsParser
    MAP_LISTS = BaseSpider.MAP_SCRAPER[name]

    def start_requests(self):
        for market in self.MAP_LISTS:
            yield scrapy.Request(url=market['url'], meta={'market': market})

    def parse(self, response, **kwargs):
        for i in json.loads(response.text)['tokens']:
            contract = dict()
            for fields in self.parser_contract.FIELDS_CONTRACT:
                _p = self.parser_contract(item=i)
                contract[fields[1]] = getattr(_p, fields[0])
            contract['marketId'] = response.meta['market']['id']
            yield contract
