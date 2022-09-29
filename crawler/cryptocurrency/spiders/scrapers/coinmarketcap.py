import re
import json
import scrapy
from datetime import datetime

from ..parsers import (
    CoinMarketCapParser,
    CoinMarketCapContractsParser,
)
from .base import BaseSpider


class CoinMarketCapSpider(BaseSpider):
    name = 'coinmarketcap'
    market = BaseSpider.MAP_SCRAPER[name]
    allowed_domains = ['coinmarketcap.com']
    headers = {
        'authority': 'api.coinmarketcap.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/'
                  'webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    parser = CoinMarketCapParser
    parser_contract = CoinMarketCapContractsParser
    start_urls = [
        'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=10000&sortBy=market_cap&'
        'sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false&'
        'aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,'
        'total_supply,volume_7d,volume_30d,volume_60d,tags'
    ]
    # Price extract
    #url_price = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={cm_id}&range={range}'
    #MAP_RANGE_DATE = ('1D', '7D', '1M', '3M', 'YTD', 'ALL',)

    async def parse(self, response, **kwargs):
        data = json.loads(response.text)['data']['cryptoCurrencyList']
        for item in data:
            yield scrapy.Request(
                url=f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?id={item['id']}",
                headers=self.headers,
                callback=self.get_item,
                meta={'meta': item}
            )

    async def get_item(self, response):
        item = dict()
        contracts = list()
        # EXTRACT new cryptocurrency
        data = json.loads(response.text)['data']
        for fields in self.parser.FIELDS:
            item[fields] = getattr(self.parser(data=data), fields)
        # EXTRACT contracts
        if data.get('platforms'):
            for _c in data['platforms']:
                contract = dict()
                _p = self.parser_contract(data=data, contract=_c)
                for fields in self.parser_contract.FIELDS_CONTRACT:
                    contract[fields[1]] = getattr(_p, fields[0])
                if _p.valid_contract:
                    contracts.append(contract)
            item['contracts'] = contracts
        yield item
        # item['price'] = list()
        # for r in self.MAP_RANGE_DATE:
        #     yield scrapy.Request(
        #         url=self.url_price.format(cm_id=item['cm_id'], range=r),
        #         callback=self.get_price,
        #         meta={'item': item},
        #     )

    # def get_price(self, response):
    #     item = response.meta['item']
    #     item['price'] += self.get_history_price(data=json.loads(response.text))
    #     # if self._next_range(url=response.url):
    #     #     yield scrapy.Request(
    #     #         url=self.url_price.format(cm_id=item['cm_id'], range=self._next_range(url=response.url)),
    #     #         callback=self.get_price,
    #     #         meta={'item': item, 'download_delay': 0},
    #     #     )
    #     # else:
    #     yield item

    # @staticmethod
    # def get_history_price(data: dict) -> list:
    #     history_price = list()
    #     if not int(data['status']['error_code']):
    #         for k, v in data['data']['points'].items():
    #             value = {
    #                 'date_time': datetime.fromtimestamp(int(k)),
    #                 'price': v['v'][0],
    #             }
    #             history_price.append(value)
    #     return history_price
    #
    # @classmethod
    # def _next_range(cls, url: str):
    #     _r = re.findall(r'range=(.+)$', url)
    #     if _r:
    #         _index = cls.MAP_RANGE_DATE.index(_r[0])
    #         try:
    #             return cls.MAP_RANGE_DATE[_index+1]
    #         except IndexError:
    #             pass
