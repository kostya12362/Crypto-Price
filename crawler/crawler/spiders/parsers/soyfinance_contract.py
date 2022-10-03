from typing import (
    Union,
)
from .base import BaseParser
from .detect_network import detect_network


class SoyFinanceContractsParser(BaseParser):

    def __init__(self, item):
        self.item = item

    @property
    def name(self) -> str:
        return self.item['name']

    @property
    def symbol(self) -> str:
        return self.item['symbol']

    @property
    def name_network(self):
        name_network, _ = detect_network(
            name_network='Callisto Mainnet',
            chain_id=self.chain_id,
            contract_address=self.contract_address
        )
        return name_network

    @property
    def decimals(self) -> int:
        return int(self.item['decimals'])

    @property
    def contract_address(self) -> str:
        return self.item['id']

    @property
    def chain_id(self) -> int:
        return 820

    @property
    def block_explorer_url(self) -> Union[str, None]:
        return f'https://explorer.callisto.network/address/{self.item["id"]}/transactions'

    @property
    def rpc_node_url(self) -> Union[list, None]:
        return

    @property
    def cm_id(self) -> Union[int, None]:
        return

    @property
    def logo_url(self) -> Union[str, None]:
        return f'https://app.soy.finance/images/coins/820/{self.item["id"]}.png'

    @property
    def logo_url_network(self) -> str:
        return f'https://app.soy.finance/images/networks/clo.png'
