import re
from typing import Union
from .base import BaseParser
from ..utils.network import detect_network


class CoinMarketCapContractsParser(BaseParser):

    def __init__(self, data: dict, contract: dict = None):
        self.data = data
        self._contract = contract

    @property
    def __clear_network_name(self):
        chain_id = self._contract.get('contractChainId') if self._contract.get('contractChainId') >= 1 else None
        name_network = self._contract.get('contractPlatform')
        return detect_network(
            name_network=name_network,
            chain_id=chain_id,
            contract_address=self._not_clear_contract_address
        )

    @property
    def name(self) -> str:
        return self.data['name']

    @property
    def symbol(self) -> str:
        return self.data['symbol']

    @property
    def name_network(self) -> str:
        name_network, _ = self.__clear_network_name
        return name_network

    @property
    def decimals(self) -> Union[int, None]:
        return self._contract.get('contractDecimals')

    @property
    def _not_clear_contract_address(self):
        return self._contract.get('contractAddress')

    @property
    def contract_address(self) -> str:
        return re.sub(r'(\(.+)$', '', self._not_clear_contract_address)

    @property
    def chain_id(self) -> Union[int, None]:
        _, chain_id = self.__clear_network_name
        return chain_id

    @property
    def block_explorer_url(self) -> Union[str, None]:
        return self._contract.get('contractExplorerUrl')

    @property
    def rpc_node_url(self) -> Union[list, None]:
        _v = self._contract.get('contractRpcUrl')
        return _v if _v else None

    @property
    def logo_url(self) -> Union[str, None]:
        return f"https://s2.coinmarketcap.com/static/img/coins/64x64/" \
               f"{self.data['id']}.png"

    @property
    def logo_url_network(self) -> Union[str, None]:
        return f"https://s2.coinmarketcap.com/static/img/coins/64x64/{self._contract.get('platformCryptoId')}.png"

    @property
    def valid_contract(self) -> bool:
        if self.contract_address:
            return True
        return False
