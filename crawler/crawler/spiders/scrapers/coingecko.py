import re
import scrapy
from ..parsers import (
    CoinGeckoParser,
    CoinGeckoContractsParser,
)
from .base import BaseSpider


class CoingeckoSpider(BaseSpider):
    name = 'coingecko'
    market = BaseSpider.MAP_SCRAPER[name]
    allowed_domains = ['coingecko.com']
    parser = CoinGeckoParser
    parser_contract = CoinGeckoContractsParser

    url = 'https://www.coingecko.com/en/all-cryptocurrencies/show_more_coins?page={page}&per_page=300&'


    def start_requests(self):
        yield scrapy.Request(self.url.format(page=1))

    def parse(self, response, **kwargs):
        hrefs = list(set([re.sub(r'(\/usd)$', '', i) for i in response.xpath('//a/@href').getall()]))
        hrefs = ['/en/coins/defi-yield-protocol']
        for href in hrefs:
            yield scrapy.Request(url=response.urljoin(href), callback=self.get_item)
        # if len(hrefs) == 300:
        #     yield scrapy.Request(url=self.url.format(page=int(re.findall(r'page=(\d+)', response.url)[0]) + 1))

    def get_item(self, response):
        item = dict()
        for fields in self.parser.FIELDS:
            item[fields] = getattr(self.parser(response=response), fields)

        contracts = list()
        for _c in self.parser_contract(response=response).get_info.xpath('descendant::div//i'):
            contract = dict()
            _p = self.parser_contract(response=response, contract=_c)
            for fields in self.parser_contract.FIELDS_CONTRACT:
                contract[fields[1]] = getattr(_p, fields[0])
            if _p.valid_contract:
                contracts.append(contract)
        item['contracts'] = contracts
        yield item
