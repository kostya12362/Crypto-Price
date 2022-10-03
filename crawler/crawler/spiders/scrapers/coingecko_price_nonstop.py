import json
import re

import scrapy
from datetime import datetime
from scrapy.utils.project import get_project_settings

from .base import BaseSpider
from .base_nonstop import BaseNonStopSpider
from ..pipelines.base import BasePipeline

settings = get_project_settings()


class CoingeckoPriceNonStopSpider(BaseNonStopSpider):
    name = 'coingecko-price'
    market = BaseSpider.MAP_SCRAPER['coingecko']
    allowed_domains = ['coingecko.com']
    download_delay = 1
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page={page}'
    start_urls = [
        url.format(page=1)
    ]
    TIME_SLEEP = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = BasePipeline(db_url=settings['POSTGRES_URL'], *args, **kwargs)

    async def parse(self, response, **kwargs):
        collected = await self.db.get_last_price(market_id=self.market['marketId'])
        data = json.loads(response.text)
        if len(data):
            for i in data:
                try:
                    if i['current_price'] != collected[i['id']]['price']:
                        item = {
                            'date_time': datetime.strptime(i['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                            'cryptocurrencyId': collected[i['id']]['id'],
                            'price': i['current_price'],
                            'marketId': self.market['marketId'],
                        }
                        yield item
                except Exception as error:
                    if 'list index out of range' in str(error):
                        print(response.url, i['image'])
                    pass
            yield scrapy.Request(url=self.next_page(response.url))

    @classmethod
    def next_page(cls, url: str):
        page = int(re.findall(r"page=(\d+)$", url)[0]) + 1
        return cls.url.format(page=page)
