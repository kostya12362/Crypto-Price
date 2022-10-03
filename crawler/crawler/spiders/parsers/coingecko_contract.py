import json
from typing import Union
from .base import BaseParser
from .detect_network import detect_network


class CoinGeckoContractsParser(BaseParser):

    def __init__(self, response, contract=None):
        self.response = response
        self._contract = contract

    @property
    def get_info(self):
        xpath = '//div[@data-target="coins-information.mobileOptionalInfo"]/div[contains(@class, "coin-link-row")]'
        return self.response.xpath(xpath)

    @property
    def get_from_json(self):
        xpath = '//script[@type="application/ld+json"][2]/text()'
        return json.loads(self.response.xpath(xpath).get())

    # FIELDS
    @property
    def name(self) -> Union[str, None]:
        return self.get_from_json['name']

    # FIELDS
    @property
    def symbol(self) -> Union[str, None]:
        return self.get_from_json['currency']

    @property
    def __clear_network_name(self):
        xpath_chain_id = 'following-sibling::img/@data-chain-id'
        xpath_network = 'parent::div/div[2]//span/text()'
        chain_id = self._contract.xpath(xpath_chain_id).get()
        return detect_network(
            name_network=self._contract.xpath(xpath_network).get(),
            chain_id=int(chain_id) if chain_id else None,
            contract_address=self.contract_address
        )

    @property
    def name_network(self) -> Union[str, None]:
        name_network, _ = self.__clear_network_name
        return name_network

    @property
    def decimals(self) -> Union[int, None]:
        xpath = 'following-sibling::img/@data-decimals'
        _d = self._contract.xpath(xpath).get()
        if _d:
            return int(_d)

    @property
    def contract_address(self):
        xpath = '@data-address'
        return self._contract.xpath(xpath).get()

    @property
    def chain_id(self) -> Union[int, None]:
        _, chain_id = self.__clear_network_name
        if chain_id:
            return int(chain_id)

    @property
    def logo_url(self) -> Union[str, None]:
        xpath = '//img[@class="tw-rounded-full"]/@src'
        return self.response.xpath(xpath).get()

    @property
    def logo_url_network(self) -> str:
        xpath = 'parent::div//@src'
        return self._contract.xpath(xpath).get()

    @property
    def block_explorer_url(self) -> Union[str, None]:
        return

    @property
    def rpc_node_url(self) -> Union[list, None]:
        return

    @property
    def valid_contract(self) -> bool:
        if self.logo_url_network and self.contract_address:
            return True
        return False
