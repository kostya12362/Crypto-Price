from tortoise import (
    Model,
    fields,
    transactions,
)
from tortoise.contrib.postgres.fields import ArrayField
from typing import (
    Optional,
)
from utils.db_extract import db_extract
from contract.schemas import (
    ContractSchemas,
)


class Contract(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=512, null=True)
    symbol = fields.CharField(max_length=512, null=True)
    contract_address = fields.CharField(max_length=512, null=True)
    decimals = fields.IntField(null=True)
    block_explorer_url = fields.CharField(max_length=1024, null=True)
    chain_id = fields.IntField(null=True)
    logo_url = fields.TextField(null=True)
    rpc_node_url = ArrayField(element_type="text", null=True)
    is_bridge = fields.BooleanField(default=False)
    cryptocurrency = fields.ForeignKeyField('models.Cryptocurrency', null=True, on_delete=fields.CASCADE)
    network = fields.ForeignKeyField('models.Network', null=True, on_delete=fields.CASCADE)
    network_name = fields.CharField(max_length=512, null=True)
    network_logo_url = fields.TextField(max_length=512, null=True)
    market = fields.ForeignKeyField('models.Market', null=True, on_delete=fields.CASCADE)

    class Meta:
        table = "contract"

    @classmethod
    async def create_contract(cls, item: ContractSchemas) -> dict:
        async with transactions.in_transaction('default') as conn:
            val = await conn.execute_query_dict('''
                    INSERT INTO "contract" (
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
                        network_id, market_id ;
                ''', (
                item.name,
                item.symbol,
                item.contractAddress,
                item.decimals,
                item.blockExplorerURL,
                item.networkName,
                item.networkLogoURL,
                item.chainId,
                item.logoURL,
                item.rpcNodeURL,
                item.bridge,
                item.cryptocurrencyId,
                item.networkId,
                item.marketId,))
            return db_extract(val)

    @classmethod
    async def get_contracts(
            cls,
            symbol: Optional[str] = None,
            name: Optional[str] = None,
            contract_address: Optional[str] = None,
    ):

        contract_address = f"{contract_address}%" if contract_address else None
        name = f"{name}%" if name else None
        symbol = symbol if symbol else None
        async with transactions.in_transaction('default') as conn:
            val = await conn.execute_query_dict('''
                select * from get_contracts(
                    _contract_address := $1,
                    _name := $2,
                    _symbol := $3
                )
                limit 300;
                ''', (
                contract_address,
                name,
                symbol,
            ))
        return db_extract(val, to_list=True)


class MergeCryptocurrency(Model):
    id = fields.IntField(pk=True, index=True)
    from_cryptocurrency = fields.ForeignKeyField("models.Cryptocurrency", related_name='from_cryptocurrency')
    to_cryptocurrency = fields.ForeignKeyField("models.Cryptocurrency", related_name='to_cryptocurrency')

    class Meta:
        table = "merge_cryptocurrency"
