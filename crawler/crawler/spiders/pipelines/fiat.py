import asyncio
import json
import logging
from .base import FiatBasePipeline

logger = logging.getLogger(__name__)


class ExchangeRateSavePipeline(FiatBasePipeline):
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
        asyncio.get_event_loop().create_task(self.conn.close())
        logger.info('======================== CLOSE SPIDER ========================')

    async def process_item(self, item, spider):
        await self.insert_or_update_fiat(item=item, market=self.market)
        return item

