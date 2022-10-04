import json
import re
import scrapy
from scrapy.utils.project import get_project_settings
from .base import BaseSpider
from .base_nonstop import BaseNonStopSpider
from ..pipelines.base import BasePipeline
from ..parsers.soyfinance import SoyFinanceParser
from ..parsers.soyfinance_contract import SoyFinanceContractsParser
import datetime
from datetime import datetime

settings = get_project_settings()


class SoyFinanceSpider(BaseNonStopSpider):
    name = 'soyfinance-price'
    market = BaseSpider.MAP_SCRAPER['soyfinance']
    allowed_domains = ['03.callisto.network']
    parser = SoyFinanceParser
    parser_contract = SoyFinanceContractsParser
    url = 'https://03.callisto.network/subgraphs/name/soyswap'
    TIME_SLEEP = 600
    start_urls = [
        url
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = BasePipeline(db_url=settings['POSTGRES_URL'], *args, **kwargs)

    async def parse(self, response, **kwargs):
        collected = await self.db.get_last_price(market_id=self.market['marketId'])
        yield scrapy.Request(url=self.url, method='POST', body=json.dumps(self.token_body(contracts=list(collected.keys()))),
                             callback=self.get_detail, meta={'collected': collected})

    def get_detail(self, response):
        data = json.loads(response.text)
        collected = response.meta['collected']
        for i in data['data']['tokens']:
            if collected[i['id']]['price'] != i['derivedUSD']:
                item = {
                    'date_time': datetime.now(),
                    'cryptocurrencyId': collected[str(i['id'])]['id'],
                    'price': float(re.findall(r'\d+.\d{6}', i['derivedUSD'])[0]),
                    'marketId': self.market['marketId'],
                }
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

