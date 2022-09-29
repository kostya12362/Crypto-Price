from pathlib import Path
from twisted.internet import asyncioreactor

asyncioreactor.install()

BASE_DIR = Path(__file__).resolve().parent

BOT_NAME = 'cryptocurrency'

SPIDER_MODULES = ['cryptocurrency.spiders']
NEWSPIDER_MODULE = 'cryptocurrency.spiders'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

ROBOTSTXT_OBEY = False
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

LOG_LEVEL = 'INFO'

ASYNCIO_EVENT_LOOP = True

POSTGRES_URL = 'postgres://postgres:DFjuHWwXMHDWMGd5g@localhost:5432/absolute_wallet'
# CRYPTOCURRENCY_SAVE_URL = 'http://0.0.0.0:5006/cryptocurrency/save'
# MARKET_SAVE_URL = 'http://localhost:5006/market/save'
# FIAT_SAVE_URL = 'http://localhost:5006/fiat/save'
# CONTRACT_SAVE_URL = 'http://localhost:5006/contract/save'
# PRICE_SAVE_URL = 'http://localhost:5006/price/save'