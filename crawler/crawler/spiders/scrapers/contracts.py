import json

import scrapy

from ..parsers import ListContractsParser
from .base import BaseSpider


class CoinmarketcapSpider(scrapy.Spider):
    name = 'contracts'
    handle_httpstatus_list = [422, 500]
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.spiders.pipelines.contracts.ContractsSavePipeline': 300
        }
    }
    parser_contract = ListContractsParser
    MAP_LISTS_MARKET = BaseSpider.MAP_SCRAPER[name]

    def start_requests(self):
        for market in self.MAP_LISTS_MARKET:
            yield scrapy.Request(url=market['url'], meta={'market': market})

    async def parse(self, response, **kwargs):
        for i in json.loads(response.text)['tokens']:
            contract = dict()
            for fields in self.parser_contract.FIELDS_CONTRACT:
                _p = self.parser_contract(item=i)
                contract[fields[1]] = getattr(_p, fields[0])
            contract['marketId'] = response.meta['market']['marketId']
            print(contract)
            yield contract
