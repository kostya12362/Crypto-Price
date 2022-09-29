import datetime
import unicodedata
from typing import Union
from .base import BaseParser


class SoyFinanceParser(BaseParser):

    def __init__(self, item: dict):
        self.item = item

    # FIELDS
    @property
    def name(self) -> str:
        return self.item['name']

    # FIELDS
    @property
    def symbol(self) -> str:
        return self.item['symbol']

    # FIELDS
    @property
    def slug(self) -> Union[str, None]:
        return unicodedata.normalize('NFKD', f"{self.item['name']} {self.item['symbol']}").lower().replace(' ', '-')

    # FIELDS
    @property
    def date_added(self) -> Union[datetime.datetime, None]:
        return

    # FIELDS
    @property
    def logo_url(self) -> Union[str, None]:
        return f'https://app.soy.finance/images/coins/820/{self.item["id"]}.png'

    # FIELDS_META
    @property
    def rank(self) -> None:
        return

    # FIELDS_META
    @property
    def tags(self) -> None:
        return

    # FIELDS_META
    @property
    def cm_id(self) -> None:
        return

    # FIELDS_META
    @property
    def website(self) -> None:
        return

    # FIELDS_META
    @property
    def source_code(self) -> None:
        return

    # FIELDS_META
    @property
    def explorers(self) -> Union[list, None]:
        return [f'https://explorer.callisto.network/address/{self.item["id"]}/transactions']

    # FIELDS_META
    @property
    def community(self) -> None:
        return

    # FIELDS_META
    @property
    def search_on(self) -> None:
        return

    # FIELDS_META
    @property
    def wallets(self) -> None:
        return

    # FIELDS_META
    @property
    def stars(self) -> None:
        return

    # FIELDS_META
    @property
    def technical_doc(self) -> None:
        return

    # FIELDS_META
    @property
    def audit_infos(self) -> None:
        return


