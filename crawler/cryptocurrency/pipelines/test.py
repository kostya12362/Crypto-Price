import json
import asyncio
import logging
from .base import BasePipeline

logger = logging.getLogger(__name__)


class CryptocurrencySavePipeline(BasePipeline):

    def __init__(self, market: dict, db_url: str):
        super().__init__(db_url=db_url)
        self.market = market

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            market=crawler.spidercls.market,
            db_url=crawler.settings['POSTGRES_URL']
        )

    def open_spider(self, spider):
        logger.info('======================== CREATE NEW MARKET ========================')
        val = asyncio.get_event_loop().run_until_complete(self.insert_new_market(market=self.market))
        logger.info(json.dumps(val))

    def close_spider(self, spider):
        asyncio.get_event_loop().create_task(self.close())
        logger.info('======================== CLOSE SPIDER ========================')

    async def process_item(self, item, spider):
        val = await self.insert_new_item(item=item, market=self.market)
        # save contract
        if item.get('contracts'):
            async def create_contract(contract: dict):
                contract['cryptocurrencyId'] = val
                await self.insert_contract(contract=contract, market=self.market)

            tasks = [create_contract(contract=contract) for contract in item['contracts']]
            await asyncio.gather(*tasks)
        # save price history
        # if item.get('price'):
        #     await self.insert_many_history_price(price=item['price'], market=self.market, cryptocurrency_id=val)
        # async def create_history_price(price: dict):
        #     price['cryptocurrencyId'] = val
        #     await self.insert_history_price(price=price, market=self.market)
        # tasks = [create_history_price(price=price) for price in item['price']]
        # await asyncio.gather(*tasks)
