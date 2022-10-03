import asyncio
import logging

from .base import BasePipeline

logger = logging.getLogger(__name__)


class PriceSavePipeline(BasePipeline):

    def __init__(self, db_url: str):
        super().__init__(db_url=db_url)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_url=crawler.settings['POSTGRES_URL']
        )

    def open_spider(self, spider):
        logger.info('======================== OPEN SPIDER ========================')

    def close_spider(self, spider):
        asyncio.get_event_loop().create_task(self.close())
        logger.info('======================== CLOSE SPIDER ========================')

    async def process_item(self, item, spider):
        await self.insert_history_price(item=item)
        return item
