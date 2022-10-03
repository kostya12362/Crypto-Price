from typing import (
    List,
)
from tortoise import (
    Model,
    fields,
    transactions,
)
from utils.db_extract import db_extract


class Price(Model):
    id = fields.IntField(pk=True, index=True)
    date_time = fields.DatetimeField()
    price = fields.FloatField()
    market = fields.ForeignKeyField('models.Market', on_delete=fields.CASCADE)
    cryptocurrency = fields.ForeignKeyField('models.Cryptocurrency', on_delete=fields.CASCADE)

    class Meta:
        table = "history_price"

    @classmethod
    async def get_last_value(cls, symbols: List[str], fiat: str):
        async with transactions.in_transaction("default") as conn:
            val = await conn.execute_query_dict('''
SELECT cr.id   as "id",
       cr.name,
       cr.symbol,
       cr.tags,
       CASE
           WHEN (hp.price is not null) THEN jsonb_build_object(
                   'lastUpdate', date_time,
                   'priceFiat', hp.price * coalesce((select value from fiat as f where f.code = $2), 1)
               )
           END as "price",
       
       jsonb_build_object(
            'marketId', m2.id,
            'marketName', m2.name,
            'marketLogoURL', m2.logo,
            'marketSite', m2.site
       ) as "market"
FROM (select * from cryptocurrency where symbol::citext = any($1::citext[])) AS cr
         LEFT JOIN LATERAL ( select  date_time,
                                    h.price,
                                    m1.id as "idm",
                                    m1.name,
                                    m1.logo,
                                    m1.site,
                                    h.cryptocurrency_id
                             from history_price as h
                                      left join market m1 on h.market_id = m1.id
                             where h.cryptocurrency_id = cr.id
                             ORDER BY h.cryptocurrency_id, h.date_time DESC LIMIT 1
    ) as hp on true
    INNER JOIN market m2 on m2.id = cr.market_id
    ORDER BY cr.cm_id::int''', (symbols, fiat,))
            return db_extract(val, to_list=True)
