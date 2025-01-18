from time import sleep

from scrapy.downloadermiddlewares.retry import RetryMiddleware


class DelayedRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if response.status == 429 or response.status == 420:
            self.crawler.engine.pause()
            sleep(3660)
            self.crawler.engine.unpause()
        return super().process_response(request, response, spider)
