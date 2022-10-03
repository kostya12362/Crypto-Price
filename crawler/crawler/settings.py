import os
from pathlib import Path
from twisted.internet import asyncioreactor

asyncioreactor.install()

ASYNCIO_EVENT_LOOP = True
ROBOTSTXT_OBEY = False
BASE_DIR = Path(__file__).resolve().parent

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

LOG_LEVEL = 'INFO'

POSTGRES_DB = os.getenv('POSTGRES_DB', 'absolute')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'DFjuHWwXMHDWMGd5g')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))

POSTGRES_URL = f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
