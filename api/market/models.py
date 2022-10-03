from tortoise import (
    Model,
    fields,
    transactions,
)

from utils.db_extract import db_extract


class Market(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=256, unique=True)
    logo = fields.TextField(null=True)
    site = fields.TextField(null=True)
    create = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "market"

    @classmethod
    async def get_markets(cls):
        async with transactions.in_transaction("default") as conn:
            val = await conn.execute_query_dict('''
                            SELECT
                                m.id as "marketId",
                                m.name as "marketName",
                                m.logo as "marketLogoURL",
                                m.site as "marketSite",
                                m.create as "marketCreated"
                            FROM market as m;
                        ''', ())
            return db_extract(val, to_list=True)
