from time import sleep

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message


class DelayedRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)

            sleep(3600)

            return self._retry(request, reason, spider) or response

        return response
