import json
from tortoise import (
    Model,
    fields,
    transactions,
)
from tortoise.contrib.postgres.fields import ArrayField

from utils.db_extract import db_extract
from cryptocurrency.schemas import CryptocurrencySchemas


class Cryptocurrency(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=512, null=True)
    symbol = fields.CharField(max_length=512, null=True)
    slug = fields.CharField(max_length=512, null=True)
    date_added = fields.DatetimeField(null=True)
    logo_url = fields.TextField(null=True)
    # meta data
    market = fields.ForeignKeyField('models.Market', null=True, on_delete=fields.CASCADE)
    cm_id = fields.CharField(max_length=512, null=True)
    rank = fields.IntField(null=True)
    stars = fields.IntField(null=True)
    tags = ArrayField(element_type="text", null=True)
    website = ArrayField(element_type="text", null=True)
    community = ArrayField(element_type="text", null=True)
    explorers = ArrayField(element_type="text", null=True)
    source_code = ArrayField(element_type="text", null=True)
    technical_doc = ArrayField(element_type="text", null=True)
    audit_infos = fields.JSONField(null=True)

    class Meta:
        table = "cryptocurrency"

    @classmethod
    async def create_cryptocurrency(cls, item: CryptocurrencySchemas):
        async with transactions.in_transaction('default') as conn:
            val = await conn.execute_query_dict('''
                INSERT INTO "cryptocurrency" (
                    name, symbol, slug, date_added, logo_url, market_id, cm_id, rank, stars, tags, website, community,
                    explorers, source_code, technical_doc, audit_infos
                )
                VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
                ON CONFLICT (name, symbol, slug, market_id) DO
                UPDATE set
                    date_added = EXCLUDED.date_added,
                    logo_url = EXCLUDED.logo_url,
                    cm_id = EXCLUDED.cm_id,
                    rank = EXCLUDED.rank,
                    stars = EXCLUDED.stars,
                    tags = EXCLUDED.tags,
                    website = EXCLUDED.website,
                    community = EXCLUDED.community,
                    explorers = EXCLUDED.explorers,
                    source_code = EXCLUDED.source_code,
                    technical_doc = EXCLUDED.technical_doc,
                    audit_infos = EXCLUDED.audit_infos
                RETURNING id as "id", name, symbol, slug, date_added as "dateAdded",
                 logo_url as "logoURL", market_id as "marketId";
            ''', (
                item.name, item.symbol, item.slug, item.date_added, item.logo_url, item.marketId, item.cm_id, item.rank,
                item.stars, item.tags, item.website, item.community, item.explorers, item.source_code,
                item.technical_doc, json.dumps(item.audit_infos) if item.audit_infos else None
            ))
            return db_extract(val)

    @classmethod
    async def get_cryptocurrency(cls, limit: bool):
        async with transactions.in_transaction('default') as conn:
            val = await conn.execute_query_dict(f'''
                SELECT 
                    cr1. id                                    as "id",
                    cr1.name                                   as "name",
                    cr1.market_id                              as "marketId",
                    cr1.cm_id                                  as "cmId",
                    cr1.symbol                                 as "symbol",
                    cr1.slug                                   as "slug",
                    cr1.date_added                             as "dateAdded",
                    cr1.logo_url                               as "logoURL",
                    cr1.rank                                   as "rank",
                    jsonb_build_object(
                           'stars', cr1.stars,
                           'tags', cr1.tags,
                           'website', cr1.website,
                           'community', cr1.community,
                           'explorers', cr1.explorers,
                           'source_code', cr1.source_code,
                           'audit', cr1.audit_infos
                       )                                       as "meta"
                FROM cryptocurrency AS cr1
                ORDER BY cr1.rank nulls last
                {'LIMIT 100;' if limit else ';'}
            ''', ())
            return db_extract(val, to_list=True)

    @classmethod
    async def get_like_cryptocurrency(cls, symbol):
        async with transactions.in_transaction('default') as conn:
            val = await conn.execute_query_dict('''
select mr.f                                                       as "id",
       (array_agg(cr1.name))[1]                                   as "name",
       (array_agg(cr1.market_id))[1]                              as "marketId",
       (array_agg(cr1.cm_id))[1]                                  as "cmId",
       (array_agg(cr1.symbol))[1]                                 as "symbol",
       (array_agg(cr1.slug))[1]                                   as "slug",
       (array_agg(cr1.date_added))[1]                             as "dateAdded",
       (array_agg(cr1.logo_url))[1]                               as "logoURL",
       (array_agg(cr1.rank))[1]                                   as "rank",
       jsonb_build_object(
               'stars', jsonb_agg(distinct cr1.stars) -> 0,
               'tags', jsonb_agg(distinct cr1.tags) -> 0,
               'website', jsonb_agg(distinct cr1.website) -> 0,
               'community', jsonb_agg(distinct cr1.community) -> 0,
               'explorers', jsonb_agg(distinct cr1.explorers) -> 0,
               'source_code', jsonb_agg(distinct cr1.source_code) -> 0,
               'audit', jsonb_agg(distinct cr1.audit_infos) -> 0
           )                                                      as meta,
       nullif(array_remove(array_agg(distinct mr.t), null), '{}') as groups,
       (CASE
            WHEN (array_agg(con."contractAddress"))[1] is not null THEN
                jsonb_agg(
                        distinct jsonb_build_object(
                        'id', con.id,
                        'name', con.name,
                        'symbol', con.symbol,
                        'contractAddress', con."contractAddress",
                        'networkName', con."networkName",
                        'networkLogoURL', con."networkLogoURL",
                        'chainId', con."chainId",
                        'decimals', con.decimals,
                        'rpcNodeURL', nullif(con."rpcNodeURL", '{}'),
                        'blockExplorerURL', con."blockExplorerURL",
                        'markets', con.markets
                    )
                    )
            ELSE
                '[]'::jsonb
           END
           )                                                      as "contracts"
from marge_clean() mr
         left join (select * from get_contracts() where name is not null and "contractAddress" is not null) con
                   on mr.f = con."cryptocurrencyId" or
                      mr.t = con."cryptocurrencyId"
         left join cryptocurrency as cr1 on mr.f = cr1.id or mr.f = cr1.id
where cr1.symbol = $1
group by mr.f
order by (array_agg(cr1.market_id))[1], (array_agg(cr1.rank))[1] nulls last,
         array_length(nullif(array_remove(array_agg(distinct mr.t), null), '{}'), 1)
limit 5;
            ''', (symbol,))
        return db_extract(val, to_list=True)
