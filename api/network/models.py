import re

from tortoise.contrib.postgres.fields import ArrayField
from tortoise import (
    Model,
    fields,
    transactions,
)
from db import ReadNetworkMap

from utils.db_extract import db_extract


class Network(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=512, unique=True)
    symbol = fields.CharField(max_length=512, unique=True, null=True)
    block_explorer_url = fields.TextField(null=True)
    rpc_node_url = ArrayField(element_type="text", null=True)
    chain_id = fields.IntField(null=True)
    cryptocurrency = fields.ForeignKeyField('models.Cryptocurrency', null=True, default=None, on_delete=fields.CASCADE)
    logo_url = fields.TextField(null=True, default=None)
    is_active = fields.BooleanField(default=False)
    is_contracts = fields.BooleanField(default=False)

    class Meta:
        table = "network"

    @classmethod
    async def detect_network(cls):
        reader = ReadNetworkMap()
        async with transactions.in_transaction("default") as conn:
            for i in reader():
                await conn.execute_query_dict('''
                                UPDATE network as n
                                SET cryptocurrency_id = cr.id
                                FROM cryptocurrency as cr
                                WHERE cr.cm_id = $1 and cr.market_id = 1 and n.id = $2
                                RETURNING 
                                    n.id as "id",
                                    n.name as "name",
                                    n.symbol as "symbol",
                                    n.block_explorer_url as "blockExplorerURL",
                                    n.rpc_node_url as "rpcNodeURL",
                                    n.chain_id as "chainId", 
                                    n.logo_url as "logoNetworkURL",
                                    n.is_active as "isActive";
                            ''', (re.findall(r'\/(\d+)\.', i['logoNetworkURL'])[0], i['id'],))

    @classmethod
    async def get_networks(cls):
        async with transactions.in_transaction("default") as conn:
            val = await conn.execute_query_dict('''
                SELECT
                    n.id as "id",
                    n.name as "name",
                    n.symbol as "symbol",
                    n.block_explorer_url as "blockExplorerURL",
                    n.rpc_node_url as "rpcNodeURL",
                    n.chain_id as "chainId", 
                    n.logo_url as "logoNetworkURL",
                    n.is_active as "isActive"
                FROM network as n
                WHERE n.is_active = true
            ''', ())
            return db_extract(val, to_list=True)
