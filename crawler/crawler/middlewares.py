# import os
# import json
# import scrapy
# import hashlib
# import base64
#
#
# class ProxyMiddleware:
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler.settings)
#
#     def __init__(self, settings):
#         self.user = settings.get('SMARTPROXY_USER', '10571')
#         self.password = settings.get('SMARTPROXY_PASSWORD', '10571')
#         self.endpoint = settings.get('SMARTPROXY_ENDPOINT', 'node-de-34.astroproxy.com')
#         self.port = settings.get('SMARTPROXY_PORT', 10571)
#         self._auth = 'Basic ' + base64.b64encode(f'{self.user}:{self.password}'.encode()).decode()
#
#     def process_request(self, request, spider):
#         if spider.custom_settings and spider.custom_settings.get('HTTPPROXY_ENABLED') is False:
#             return
#
#         host = 'http://{endpoint}:{port}'.format(endpoint=self.endpoint, port=self.port)
#         request.headers['Proxy-Authorization'] = self._auth
#         request.meta['proxy'] = host
#
#
# from twisted.internet import reactor, defer
# from scrapy.downloadermiddlewares.retry import RetryMiddleware
# from scrapy.utils.response import response_status_message
#
#
# async def async_sleep(delay, return_value=None):
#     deferred = defer.Deferred()
#     reactor.callLater(delay, deferred.callback, return_value)
#     return await deferred
#
#
# class TooManyRequestsRetryMiddleware(RetryMiddleware):
#     """
#     Modifies RetryMiddleware to delay retries on status 429.
#     """
#
#     DEFAULT_DELAY = 60  # Delay in seconds.
#     MAX_DELAY = 600  # Sometimes, RETRY-AFTER has absurd values
#
#     async def process_response(self, request, response, spider):
#         """
#         Like RetryMiddleware.process_response, but, if response status is 429,
#         retry the request only after waiting at most self.MAX_DELAY seconds.
#         Respect the Retry-After header if it's less than self.MAX_DELAY.
#         If Retry-After is absent/invalid, wait only self.DEFAULT_DELAY seconds.
#         """
#
#         if request.meta.get('dont_retry', False):
#             return response
#
#         if response.status in self.retry_http_codes:
#             if response.status == 429:
#                 retry_after = response.headers.get('retry-after')
#                 try:
#                     retry_after = int(retry_after)
#                 except (ValueError, TypeError):
#                     delay = self.DEFAULT_DELAY
#                 else:
#                     delay = min(self.MAX_DELAY, retry_after)
#                 spider.logger.info(f'Retrying {request} in {delay} seconds.')
#
#                 spider.crawler.engine.pause()
#                 await async_sleep(delay)
#                 spider.crawler.engine.unpause()
#
#             reason = response_status_message(response.status)
#             return self._retry(request, reason, spider) or response
#
#         return response
