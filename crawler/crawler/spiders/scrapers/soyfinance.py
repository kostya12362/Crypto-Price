import json
import re
import scrapy
from .base import BaseSpider
from ..parsers.soyfinance import SoyFinanceParser
from ..parsers.soyfinance_contract import SoyFinanceContractsParser
from typing import (
    Union,
)
import datetime
from datetime import datetime, timedelta


class SoyFinanceSpider(BaseSpider):
    name = 'soyfinance'
    market = BaseSpider.MAP_SCRAPER[name]
    allowed_domains = ['03.callisto.network']
    parser = SoyFinanceParser
    parser_contract = SoyFinanceContractsParser
    url = 'https://03.callisto.network/subgraphs/name/soyswap'
    url_js = 'https://app.soy.finance/static/js/693.2a223346.chunk.js'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.url, method='POST', body=json.dumps(self.contract_body))

    def parse(self, response, **kwargs):
        contracts = self.extract_contracts(response)
        print(contracts)
        yield scrapy.Request(url=self.url, method='POST', body=json.dumps(self.token_body(contracts=contracts)),
                             callback=self.get_detail)

    # def get_detail(self, response):
    #     yield scrapy.Request(url=self.url_js, callback=self.get_detail_js, meta={'data': json.loads(response.text)},
    #                          dont_filter=True)

    def get_detail(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        data = self.get_data_from_js(response.text)
        for token in response.meta['data']['data']['tokens']:
            item = dict()
            token['name'] = data.get(token['id'], token)['name']
            if token['symbol'] == 'unknown':
                token['symbol'] = f"cc{token['name'].split()[-1]}"
            for fields in self.parser.FIELDS:
                item[fields] = getattr(self.parser(item=token), fields)

            contracts = list()
            contract = dict()
            for fields in self.parser_contract.FIELDS_CONTRACT:
                contract[fields[1]] = getattr(self.parser_contract(item=token), fields[0])
            contracts.append(contract)
            item['contracts'] = contracts
            yield item

    @staticmethod
    def token_body(contracts):
        return {
            "query": '''
                query tokens($allTokens: [String]) {
                tokens(
                     where: {id_in: $allTokens}
                    first: 1000
                ) {
                  id
                  name
                  decimals
                  symbol
                  derivedCLO
                  derivedUSD
                  totalLiquidity
                }
              }''',
            "variables": {
                "allTokens": contracts
            }
        }

    @property
    def contract_body(self):
        return {
            "query": '''query tokens($blacklist: [String!], $timestamp24hAgo: Int) {
                tokenDayDatas(
                    first: 50
                    where: { dailyTxns_gt: 1, token_not_in: $blacklist, date_gt: $timestamp24hAgo }
                    orderBy: dailyVolumeUSD
                    orderDirection: desc
                    ) {
                        id
                }
            }''',
            "variables":
                {
                    "blacklist": ["0xffbce94c24a6c67daf7315948eb8b9fa48c5cdee"],
                    "timestamp24hAgo": int((datetime.now() - timedelta(days=1)).timestamp())
                }
        }

    @staticmethod
    def extract_contracts(response):
        return [re.sub(r"-(.+)$", '', item['id']) for item in json.loads(response.text)['data']['tokenDayDatas']]

    @staticmethod
    def get_data_from_js(text: str) -> Union[dict, None]:
        _data = re.findall(r'Ge=(.+);function', text)[0]
        if _data:
            _data = _data.replace('name:', '"name":')
            _data = _data.replace('symbol:', '"symbol":')
            return json.loads(_data)

    @staticmethod
    def hard_list():
        return
