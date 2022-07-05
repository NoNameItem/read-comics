import datetime
import json
from typing import Callable, List, Optional, Tuple, Union

import scrapy


class ResourceRequest(scrapy.Request):
    attributes: Tuple[str, ...] = (
        "url", "resource", "callback", "method", "headers", "body",
        "cookies", "meta", "encoding", "priority",
        "dont_filter", "errback", "flags", "cb_kwargs",
    )

    def __init__(self, url: str, resource: str, callback: Optional[Callable] = None, method: str = "GET",
                 headers: Optional[dict] = None, body: Optional[Union[bytes, str]] = None,
                 cookies: Optional[Union[dict, List[dict]]] = None, meta: Optional[dict] = None,
                 encoding: str = "utf-8", priority: int = 0, dont_filter: bool = False,
                 errback: Optional[Callable] = None, flags: Optional[List[str]] = None,
                 cb_kwargs: Optional[dict] = None):
        super().__init__(url, callback, method, headers, body, cookies, meta, encoding, priority, dont_filter, errback,
                         flags, cb_kwargs)
        self.resource = resource


class ImageSpider(scrapy.Spider):
    # LIST_URL_PATTERN should contain 3 placeholders: limit, offset and api_key and should not contain filter parameter
    LIST_URL_PATTERN = "https://comicvine.gamespot.com/api/{resource}/?" \
                       "format=json&" \
                       "field_list=id,name,api_detail_url,image&" \
                       "sort=id:asc&" \
                       "offset={offset}&" \
                       "limit={limit}&" \
                       "api_key={api_key}"
    LIMIT = 100
    RESOURCES = {
        "characters": "comicvine_characters",
        "concepts": "comicvine_concepts",
        "issues": "comicvine_issues",
        "locations": "comicvine_locations",
        "objects": "comicvine_objects",
        "people": "comicvine_people",
        "publishers": "comicvine_publishers",
        "story_arcs": "comicvine_story_arcs",
        "teams": "comicvine_teams",
        "volumes": "comicvine_volumes",
    }
    name = "image_spider"

    def __init__(
        self,
        api_key=None,
        mongo_url=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.api_key = api_key
        self.mongo_url = mongo_url

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.api_key = spider.api_key or spider.settings.get("API_KEY")
        spider.mongo_url = spider.mongo_url or spider.settings.get("MONGO_URL")
        spider.logger.info("Spider name: " + spider.name)
        spider.logger.info("API_KEY: " + spider.api_key)
        spider.logger.info("MONGO_URL: " + spider.mongo_url)

        return spider

    def start_requests(self):
        for resource in self.RESOURCES.keys():
            url = self.construct_list_url(resource, 0)
            yield ResourceRequest(url=url, resource=resource, callback=self.parse_list)

    def construct_list_url(self, resource, offset):
        url = self.LIST_URL_PATTERN.format(
            **{"api_key": self.api_key, "limit": self.LIMIT, "offset": offset, "resource": resource})
        self.logger.info("List url: " + url)
        return url

    def parse(self, response, **kwargs):
        pass

    def parse_list(self, response):
        # Parsing json
        json_res = json.loads(response.body)
        resource = response.request.resource

        collection_name = self.RESOURCES[resource]

        # Follow to detail pages
        for entry in json_res.get("results", []):
            entry["crawl_date"] = datetime.datetime.now()
            item = {
                "_collection": collection_name,
                "item": entry
            }
            yield item

        # Follow to next list page
        offset = json_res["offset"]
        number_of_total_results = json_res["number_of_total_results"]
        number_of_page_results = json_res["number_of_page_results"]

        if offset + number_of_page_results < number_of_total_results:
            next_page = self.construct_list_url(resource, offset + number_of_page_results)
            yield ResourceRequest(url=next_page, resource=resource, callback=self.parse_list)
