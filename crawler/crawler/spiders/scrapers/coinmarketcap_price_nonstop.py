import json

from datetime import datetime
from scrapy.utils.project import get_project_settings

from .base import BaseSpider
from .base_nonstop import BaseNonStopSpider
from ..pipelines.base import BasePipeline

settings = get_project_settings()


class CoinmarketcapPriceNonStopSpider(BaseNonStopSpider):
    name = 'coinmarketcap-price'
    market = BaseSpider.MAP_SCRAPER['coinmarketcap']
    allowed_domains = ['api.coinmarketcap.com']
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'ITEM_PIPELINES': {
            'crawler.spiders.pipelines.price.PriceSavePipeline': 320
        }
    }
    start_urls = [
        'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=10000&sortBy=market_cap&'
        'sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false'
        '&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,'
        'total_supply,volume_7d,volume_30d,volume_60d'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = BasePipeline(db_url=settings['POSTGRES_URL'], *args, **kwargs)

    async def parse(self, response, **kwargs):
        collected = await self.db.get_last_price(market_id=self.market['marketId'])
        data = json.loads(response.body)['data']['cryptoCurrencyList']
        for i in data:
            if collected.get(str(i['slug']), dict()).get('price') != i['quotes'][0]['price']:
                try:
                    item = {
                        'date_time': datetime.strptime(i['lastUpdated'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                        'cryptocurrencyId': collected[str(i['slug'])]['id'],
                        'price': i['quotes'][0]['price'],
                        'marketId': self.market['marketId'],
                    }
                    yield item
                except KeyError:
                    pass
