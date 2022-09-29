from typing import (
    Union,
)
from .base import BaseParser
from ..utils.network import detect_network


class ListContractsParser(BaseParser):

    def __init__(self, item: dict):
        self.data = item

    @property
    def name(self) -> str:
        return self.data['name']

    @property
    def symbol(self) -> str:
        return self.data['symbol']

    @property
    def decimals(self) -> int:
        return int(self.data['decimals'])

    @property
    def name_network(self) -> str:
        network_name, _ = detect_network(contract_address=self.contract_address, chain_id=self.chain_id)
        return network_name

    @property
    def contract_address(self) -> str:
        return self.data['address']

    @property
    def chain_id(self) -> int:
        return self.data['chainId']

    @property
    def block_explorer_url(self) -> None:
        return

    @property
    def rpc_node_url(self) -> None:
        return

    @property
    def logo_url(self) -> Union[str, None]:
        return self.data.get('logoURI')

    @property
    def logo_url_network(self) -> None:
        return
