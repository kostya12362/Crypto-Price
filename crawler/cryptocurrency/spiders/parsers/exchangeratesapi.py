from .base import BaseParser


class ExchangeRatesAPIParser(BaseParser):

    def __init__(self, item: dict, key: str):
        self.item = item
        self.key = key

    @property
    def symbol(self):
        return self.item.get('symbol')

    @property
    def name(self):
        return self.item.get('name')

    @property
    def symbol_native(self):
        return self.item.get('symbol_native')

    @property
    def decimal_digits(self):
        return self.item.get('decimal_digits')

    @property
    def code(self):
        return self.item.get('code', self.key)

    @property
    def name_plural(self):
        return self.item.get('name_plural')

    @property
    def value(self):
        return self.item.get('value')
