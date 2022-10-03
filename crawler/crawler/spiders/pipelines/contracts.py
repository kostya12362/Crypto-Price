import json
import asyncio
import logging

from datetime import datetime
from .base import BasePipeline

logger = logging.getLogger(__name__)


class ContractsSavePipeline(BasePipeline):

    def __init__(self, db_url: str, markets: list):
        super().__init__(db_url=db_url)
        self.markets = markets

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            markets=crawler.spidercls.MAP_LISTS_MARKET,
            db_url=crawler.settings['POSTGRES_URL']
        )

    def open_spider(self, spider):
        for market in self.markets:
            logger.info('======================== CREATE NEW MARKET ========================')
            val = asyncio.get_event_loop().run_until_complete(self.insert_new_market(market=market))
            logger.info(json.dumps(val))

    def close_spider(self, spider):
        asyncio.get_event_loop().create_task(self.close())
        logger.info('======================== CLOSE SPIDER ========================')

    async def process_item(self, item, spider):
        await self.insert_contract(contract=item, market=item)
