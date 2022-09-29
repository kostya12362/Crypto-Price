import asyncio
import asyncpg
from typing import (Optional, List)


class BasePipeline:

    def __init__(self, db_url: str, *args, **kwargs):
        self.conn = asyncio.get_event_loop().run_until_complete(self.db_connect(db_url=db_url))

    @staticmethod
    async def db_connect(db_url: str):
        return await asyncpg.create_pool(db_url)

    async def close(self):
        async with self.conn as pool:
            await pool.close()

    async def insert_new_item(self, item: dict, market: dict):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchval('''INSERT INTO "cryptocurrency" (
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
                ''', item['name'], item['symbol'], item['slug'], item['date_added'], item['logo_url'],
                                                   market['marketId'],
                                                   item['cm_id'],
                                                   item['rank'], item['stars'], item['tags'], item['website'],
                                                   item['community'], item['explorers'],
                                                   item['source_code'], item['technical_doc'],
                                                   item['audit_infos']
                                                   )
                return result

    async def insert_new_market(self, market: dict):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                val = await connection.fetchval('''
                    INSERT INTO market(id, name, logo, site, "create")
                    VALUES($1, $2, $3, $4, now())
                    ON CONFLICT (name)
                    DO UPDATE SET
                    name = excluded.name
                    RETURNING 
                        id as "marketId",
                        name as "marketName",
                        logo as "marketLogoURL",
                        site as "marketSite";
                ''', *(market['marketId'], market['marketName'], market['marketLogoURL'], market['marketSite']))
                return val

    async def insert_contract(self, contract: dict, market: dict):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                await connection.fetchval('''INSERT INTO "contract" (
                        name, symbol, contract_address, decimals, block_explorer_url, network_name, network_logo_url,
                        chain_id, logo_url,rpc_node_url, is_bridge, cryptocurrency_id, network_id, market_id 
                    )
                    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                    ON CONFLICT (contract_address, network_name, market_id) DO
                                        UPDATE set
                        name = EXCLUDED.name,
                        symbol = EXCLUDED.symbol,
                        decimals = EXCLUDED.decimals,
                        block_explorer_url = EXCLUDED.block_explorer_url,
                        network_name = EXCLUDED.network_name,
                        network_logo_url = EXCLUDED.network_logo_url,
                        logo_url = EXCLUDED.logo_url,
                        rpc_node_url = EXCLUDED.rpc_node_url,
                        network_id = EXCLUDED.network_id
                        RETURNING  id, name, symbol, contract_address, decimals, block_explorer_url, network_name,
                        network_logo_url, chain_id, logo_url, rpc_node_url, is_bridge, cryptocurrency_id,
                        network_id, market_id ;''', contract['name'], contract['symbol'], contract['contractAddress'],
                                          contract['decimals'],
                                          contract['blockExplorerURL'],
                                          contract['networkName'],
                                          contract['networkLogoURL'],
                                          contract['chainId'],
                                          contract['logoURL'],
                                          contract['rpcNodeURL'],
                                          contract.get('bridge', False),
                                          contract['cryptocurrencyId'],
                                          contract.get('networkId', None),
                                          market['marketId']
                                          )

    async def insert_history_price(self, price: dict, market: dict):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                await connection.fetchval('''
                    INSERT INTO history_price(date_time, cryptocurrency_id, price, market_id)
                    VALUES($1, $2, $3, $4)
                    ON CONFLICT (date_time, cryptocurrency_id, price, market_id) DO NOTHING
                    RETURNING "date_time", cryptocurrency_id, price;
                ''', price['date_time'], price['cryptocurrencyId'], price['price'], market['marketId'])

    async def insert_many_history_price(self, price: List[dict], market: dict, cryptocurrency_id: int):
        async def record_gen():
            for i in price:
                yield (i['date_time'], cryptocurrency_id, i['price'], market['marketId'],)

        async with self.conn.acquire() as connection:
            async with connection.transaction():
                try:
                    await connection.copy_records_to_table(
                        table_name='history_price',
                        columns=['date_time', 'cryptocurrency_id', 'price', 'market_id'],
                        records=record_gen()
                    )
                except asyncpg.exceptions.UniqueViolationError:
                    pass


class FiatBasePipeline(BasePipeline):

    async def insert_or_update_fiat(self, item: dict, market: dict):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                await connection.fetchval(
                    '''
                        INSERT INTO fiat_currency(symbol, name, symbol_native, decimal_digits,
                         code, name_plural, value, market_id)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                        ON CONFLICT (code)
                        DO UPDATE SET
                        value = excluded.value
                        RETURNING id, symbol, name, symbol_native, decimal_digits, code, name_plural, value, market_id;
                    ''',
                    item['symbol'],
                    item['name'],
                    item['symbol_native'],
                    item['decimal_digits'],
                    item['code'],
                    item['name_plural'],
                    item['value'],
                    market['marketId'],
                )
