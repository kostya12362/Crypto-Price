import json
from datetime import datetime
from typing import (
    Union,
)
from .base import BaseParser


class CoinMarketCapParser(BaseParser):

    def __init__(self, data):
        self.data = data

    # FIELDS
    @property
    def name(self) -> str:
        return self.data['name']

    # FIELDS
    @property
    def symbol(self) -> str:
        return self.data['symbol']

    # FIELDS
    @property
    def slug(self) -> str:
        return self.data['slug']

    # FIELDS
    @property
    def rank(self) -> Union[int, None]:
        _v = self.data['statistics'].get('rank')
        if not _v:
            print(self.data['id'])
        return _v if _v else None

    # FIELDS
    @property
    def tags(self) -> Union[list, None]:
        _v = self.data['tags']
        return [i['name'] for i in _v] if _v else None

    # FIELDS
    @property
    def date_added(self) -> Union[datetime, None]:
        _v = datetime.strptime(self.data['dateAdded'], "%Y-%m-%dT%H:%M:%S.%fZ")
        return _v if _v else None

    # FIELDS
    @property
    def cm_id(self) -> Union[str, None]:
        _v = self.data['id']
        return str(_v) if _v else None

    # FIELDS
    @property
    def logo_url(self) -> Union[str, None]:
        return f'https://s2.coinmarketcap.com/static/img/coins/64x64/{self.data["id"]}.png'

    # FIELDS_META
    @property
    def website(self) -> Union[list, None]:
        _v = self.data['urls']['website']
        return _v if _v else None

    # FIELDS_META
    @property
    def source_code(self) -> Union[list, None]:
        _v = self.data['urls']['source_code']
        return _v if _v else None

    # FIELDS_META
    @property
    def explorers(self) -> Union[list, None]:
        _v = self.data['urls']['explorer']
        if self.data.get('platforms'):
            _v += [i.get('contractExplorerUrl') for i in self.data.get('platforms', [])]
        return _v if _v else None

    # FIELDS_META
    @property
    def community(self):
        urls = self.data['urls']
        _v = urls['facebook'] + urls['reddit'] + urls['twitter'] + urls['chat']
        return _v if _v else None

    # FIELDS_META
    @property
    def technical_doc(self) -> Union[list, None]:
        _v = self.data['urls']['technical_doc']
        return _v if _v else None

    # FIELDS_META
    @property
    def audit_infos(self) -> Union[str, None]:
        _ai = self.data.get('auditInfos')
        if _ai:
            return json.dumps([
                {
                    'status': i.get('auditStatus'),
                    'auditor': i.get('auditor'),
                    'report_url': i.get('reportUrl'),
                    'audit_time': i.get('auditTime'),
                }
                for i in _ai
            ])

    # FIELDS_META
    @property
    def wallets(self) -> None:
        return

    # FIELDS_META
    @property
    def stars(self) -> Union[int, None]:
        _v = self.data['watchCount']
        return int(_v) if _v else None

    # FIELDS_META
    @property
    def search_on(self) -> None:
        return
