import os
from celery import Celery
from datetime import timedelta

from scrapyd_api import ScrapydAPI
from celery.schedules import crontab

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

scrapyd = ScrapydAPI(
    target='http://crawler:6801/',
    auth=('absolutewallet', 'kN2GaavuXKZjbTj6X2exYOgGSsrWkyxM')
)

app = Celery('tasks', broker='redis://:jjsja7123jdasdkk21238882jjejq@redis:6379/0')

MAP_SCRAPERS_NON_STOP = (
    'coinmarketcap-price',
    'coingecko-price',
    'soyfinance-price',
)


MAP_SCRAPERS = (
    'exchangeratesapi'
    'coinmarketcap'
    'coingecko',
    'soyfinance',
    'contracts',
)


@app.task(rate_limit='6/h')
def start_spider(*spider_name):
    for spider in spider_name:
        scrapyd.schedule('default', spider)


# @app.task()
# def check_spiders():
#     data = scrapyd.list_jobs('default')
#     _price = list()
#     for spider in data['running']:
#         if spider['spider'] in MAP_SCRAPERS_NON_STOP:
#             _price.append(spider['spider'])
#     for i in MAP_SCRAPERS_NON_STOP:
#         if i not in _price:
#             start_spider(*(i,))


app.conf.beat_schedule = {
    'run-everyday-00-00': {
        'schedule': crontab(hour=2, minute=13),
        'task': 'tasks.start_spider',
        'args': ('exchangeratesapi', 'coinmarketcap', 'coingecko',)
    },
    # 'run-everyday-30-min': {
    #     'schedule': timedelta(minutes=30),
    #     'task': 'tasks.check_spiders',
    #     'args': ()
    # },
}

app.conf.timezone = 'UTC'
