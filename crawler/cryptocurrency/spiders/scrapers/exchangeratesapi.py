import json
import scrapy
from scrapy.utils.project import get_project_settings
from ..parsers.exchangeratesapi import ExchangeRatesAPIParser
from .base import BaseSpider


class Exchangeratesapi(scrapy.Spider):
    name = 'exchangeratesapi'
    market = BaseSpider.MAP_SCRAPER[name]
    allowed_domains = ['api.exchangeratesapi.io']
    start_urls = [
        'http://api.exchangeratesapi.io/v1/latest?access_key=299d05e364bf647b20150da98a99f708'
    ]
    handle_httpstatus_list = [422]
    custom_settings = {
        'ITEM_PIPELINES': {
            'cryptocurrency.pipelines.fiat.ExchangeRateSavePipeline': 300
        }
    }
    parser = ExchangeRatesAPIParser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.BASE_DIR = settings.get('BASE_DIR')

    def parse(self, response, **kwargs):
        for k, v in json.loads(response.body)['rates'].items():
            data = ExchangeRatesAPIParser(
                item=self.value_and_symbol(symbol=k, value=v * (1 / json.loads(response.body)['rates']['USD'])),
                key=k
            )
            item = dict()
            for f in ExchangeRatesAPIParser.FIAT_FIELDS:
                item[f] = getattr(data, f)
            yield item

    def value_and_symbol(self, symbol: str, value) -> dict:
        with open(f'{self.BASE_DIR}/spiders/utils/Common-Currency.json') as file:
            data = json.load(file).get(symbol, {})
            data['value'] = value
        return data
