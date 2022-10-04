import json
import re
import scrapy
from .base import BaseSpider
from ..parsers.soyfinance import SoyFinanceParser
from ..parsers.soyfinance_contract import SoyFinanceContractsParser
import datetime
from datetime import datetime, timedelta


class SoyFinanceSpider(BaseSpider):
    name = 'soyfinance'
    market = BaseSpider.MAP_SCRAPER[name]
    allowed_domains = ['03.callisto.network']
    parser = SoyFinanceParser
    parser_contract = SoyFinanceContractsParser
    url = 'https://03.callisto.network/subgraphs/name/soyswap'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.url, method='POST', body=json.dumps(self.contract_body))

    def parse(self, response, **kwargs):
        contracts = self.extract_contracts(response)
        yield scrapy.Request(url=self.url, method='POST', body=json.dumps(self.token_body(contracts=contracts)),
                             callback=self.get_detail)

    def get_detail(self, response):
        data = json.loads(response.text)
        for token in data['data']['tokens']:
            item = dict()
            token['name'] = self.get_hard_data.get(token['id'], token)['name']
            token['symbol'] = self.get_hard_data.get(token['id'], token)['symbol']
            for fields in self.parser.FIELDS:
                item[fields] = getattr(self.parser(item=token), fields)
            contracts = list()
            contract = dict()
            for fields in self.parser_contract.FIELDS_CONTRACT:
                contract[fields[1]] = getattr(self.parser_contract(item=token), fields[0])
            contracts.append(contract)
            item['contracts'] = contracts
            yield item

    @staticmethod
    def token_body(contracts):
        return {
            "query": '''
                query tokens($allTokens: [String]) {
                tokens(
                     where: {id_in: $allTokens}
                    first: 1000
                ) {
                  id
                  name
                  decimals
                  symbol
                  derivedCLO
                  derivedUSD
                  totalLiquidity
                }
              }''',
            "variables": {
                "allTokens": contracts
            }
        }

    @property
    def contract_body(self):
        return {
            "query": '''query tokens($blacklist: [String!], $timestamp24hAgo: Int) {
                tokenDayDatas(
                    first: 50
                    where: { dailyTxns_gt: 1, token_not_in: $blacklist, date_gt: $timestamp24hAgo }
                    orderBy: dailyVolumeUSD
                    orderDirection: desc
                    ) {
                        id
                }
            }''',
            "variables":
                {
                    "blacklist": ["0xffbce94c24a6c67daf7315948eb8b9fa48c5cdee"],
                    "timestamp24hAgo": int((datetime.now() - timedelta(days=1)).timestamp())
                }
        }

    @staticmethod
    def extract_contracts(response):
        return [re.sub(r"-(.+)$", '', item['id']) for item in json.loads(response.text)['data']['tokenDayDatas']]

    @property
    def get_hard_data(self) -> dict:
        return {
            "0xf5ad6f6edec824c7fd54a66d241a227f6503ad3a": {
                "name": "Callisto Network",
                "symbol": "CLO"
            },
            "0x9fae2529863bd691b4a7171bdfcf33c7ebb10a65": {
                "name": "SOY Finance token",
                "symbol": "SOY"
            },
            "0xccc766f97629a4e14b3af8c91ec54f0b5664a69f": {
                "name": "Wrapped ETC",
                "symbol": "ccETC"
            },
            "0xccde29903e621ca12df33bb0ad9d1add7261ace9": {
                "name": "Wrapped BNB",
                "symbol": "ccBNB"
            },
            "0xcc208c32cc6919af5d8026dab7a3ec7a57cd1796": {
                "name": "Wrapped Ethereum",
                "symbol": "ccETH"
            },
            "0xcc10a4050917f771210407df7a4c048e8934332c": {
                "name": "Wrapped LINA",
                "symbol": "ccLINA"
            },
            "0xcc78d0a86b0c0a3b32debd773ec815130f9527cf": {
                "name": "Wrapped BNB (old contract)",
                "symbol": "ccBNB"
            },
            "0xcc8b04c0f7d0797b3bd6b7be8e0061ac0c3c0a9b": {
                "name": "Wrapped RACA",
                "symbol": "ccRACA"
            },
            "0xccec9f26f52e8e0d1d88365004f4f475f5274279": {
                "name": "Wrapped BAKE",
                "symbol": "ccBAKE"
            },
            "0xcc1530716a7ebecfdc7572edcbf01766f042155c": {
                "name": "Wrapped REEF",
                "symbol": "ccREEF"
            },
            "0xccebb9f0ee6d720debccee42f52915037f774a70": {
                "name": "Wrapped WSG",
                "symbol": "ccWSG"
            },
            "0xcc099e75152accda96d54fabaf6e333ca44ad86e": {
                "name": "Wrapped TWT",
                "symbol": "ccTWT"
            },
            "0xcc2d45f7fe1b8864a13f5d552345eb3f5a005fed": {
                "name": "Wrapped Cake",
                "symbol": "ccCake"
            },
            "0xcc50d400042177b9dab6bd31ede73ae8e1ed6f08": {
                "name": "Wrapped TON",
                "symbol": "ccTON"
            },
            "0xcc45afedd2065edca770801055d1e376473a871b": {
                "name": "Wrapped XMS",
                "symbol": "ccXMS"
            },
            "0x35e9a89e43e45904684325970b2e2d258463e072": {
                "name": "Ethereum Classic",
                "symbol": "ETC"
            },
            "0x09c4a1acae1b591c63691b8e62f46e2f0ed9a0f9": {
                "name": "Callisto Enterprise",
                "symbol": "ccCLOE"
            }
        }
