import re
from typing import (
    Tuple,
    Union,
)


class DetectNetwork:
    network = {
        'Callisto Mainnet': {'chain_id': 820, 'keys': ('Callisto', 'Callisto Mainnet', 'Callisto Network')},
        'Ethereum Classic': {'chain_id': 61, 'keys': ('Ethereum Classic',)},
        'BNB Smart Chain (BEP20)': {'chain_id': 56,
                                    'keys': ('BNB Smart Chain (BEP20)', 'BNB Smart Chain', 'BSC', 'BEP20')},
        'BNB Beacon Chain (BEP2)': {'chain_id': None,
                                    'keys': ('BNB Beacon Chain (BEP2)', 'BNB Beacon Chain', 'Beacon Chain')},
        'Ethereum': {'chain_id': 1, 'keys': ('Ethereum',)},
        'Radix': {'chain_id': None, 'keys': ('Radix', 'XRD',)},
        'Solana': {'chain_id': None, 'keys': ('Solana', 'SOL')},
        'Tron': {'chain_id': None, 'keys': ('TRON', 'Tron20', 'Tron10', 'TRX')},
        'Polygon': {'chain_id': 137, 'keys': ('Polygon', 'MATIX')},
        'BitTorrent': {'chain_id': 199, 'keys': ('BitTorrent', 'BTT')},
        'Avalanche': {'chain_id': 43114, 'keys': ('Avalanche C-Chain', 'Avalanche', 'AVAX')},
        'Fantom': {'chain_id': 250, 'keys': ('Fantom Opera', 'Fantom',)},
        'Harmony': {'chain_id': 1666600000, 'keys': ('Harmony',)},
        'Fuse': {'chain_id': 122, 'keys': ('Fuse',)},
        'Terra': {'chain_id': None, 'keys': ('Terra Classic',)},
        'Terra 2.0': {'chain_id': None, 'keys': ('Terra', 'Terra 2.0')},
        'Moonriver': {'chain_id': 1285, 'keys': ('Moonriver',)},
        'KCC': {'chain_id': 321, 'keys': ('KCC',)},
        ###################
        'Ropsten': {'chain_id': 3, 'keys': ('Ropsten',)},
        'Rinkeby': {'chain_id': 4, 'keys': ('Rinkeby',)},
        'Görli': {'chain_id': 5, 'keys': ('Görli',)},
        'Optimism': {'chain_id': 10, 'keys': ('Optimism',)},
        'Arbitrum One': {'chain_id': 42161, 'keys': ('Arbitrum One',)},
        'Celo': {'chain_id': 42220, 'keys': ('Celo',)},
        'Mumbai': {'chain_id': 1285, 'keys': ('Mumbai',)},
    }

    def __call__(
            self,
            contract_address,
            chain_id: int = None,
            name_network: str = None
    ) -> Tuple[Union[str, None], Union[int, None]]:

        _network = self._clear_contract_address(contract_address, name_network)
        if _network != name_network:
            chain_id = None
            name_network = _network
        for k, v in self.network.items():
            if self._check_by_keys(key=k, name_network=name_network):
                return k, v['chain_id']
            if chain_id and chain_id == v['chain_id']:
                return k, v['chain_id']

        return name_network, chain_id

    def _check_by_keys(self, key: str, name_network: str):
        try:
            if [i for i in self.network[key]['keys'] if name_network.lower() == i.lower()]:
                return key
        except AttributeError:
            pass

    @staticmethod
    def _clear_contract_address(contract_address: str, name_network: str = None):
        if name_network:
            if 'Beacon' in name_network or 'BNB' in name_network:
                if '-' in contract_address:
                    name_network = 'BNB Beacon Chain (BEP2)'
                else:
                    name_network = 'BNB Smart Chain (BEP20)'
            check_network = re.findall(r'(\(.+)$', contract_address)
            if check_network:
                return check_network[0].replace('(', '').replace(')', '')
        return name_network


detect_network = DetectNetwork()
