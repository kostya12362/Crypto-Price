# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name='Crawler',
    version='1.0.1',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = crawler.settings']},
)
