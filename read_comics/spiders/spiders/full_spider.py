import datetime
import json
import random
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple, Union

import scrapy

from ..mongo_connection import Connect


class SpiderImplementationError(Exception):
    pass


@dataclass
class Endpoint:
    collection: str
    endpoint: str
    list_url_fields: str
    detail_url_fields: str


class EndpointRequest(scrapy.Request):
    attributes: Tuple[str, ...] = (
        "url",
        "endpoint",
        "callback",
        "method",
        "headers",
        "body",
        "cookies",
        "meta",
        "encoding",
        "priority",
        "dont_filter",
        "errback",
        "flags",
        "cb_kwargs",
    )

    def __init__(
        self,
        url: str,
        endpoint: Endpoint,
        callback: Optional[Callable] = None,
        method: str = "GET",
        headers: Optional[dict] = None,
        body: Optional[Union[bytes, str]] = None,
        cookies: Optional[Union[dict, List[dict]]] = None,
        meta: Optional[dict] = None,
        encoding: str = "utf-8",
        priority: int = 0,
        dont_filter: bool = False,
        errback: Optional[Callable] = None,
        flags: Optional[List[str]] = None,
        cb_kwargs: Optional[dict] = None,
    ):
        super().__init__(
            url,
            callback,
            method,
            headers,
            body,
            cookies,
            meta,
            encoding,
            priority,
            dont_filter,
            errback,
            flags,
            cb_kwargs,
        )
        self.endpoint = endpoint


class FullSpider(scrapy.Spider):
    ENDPOINTS = (
        Endpoint(
            "comicvine_characters",
            "characters",
            "id,api_detail_url,site_detail_url,name,aliases,deck,image,first_appeared_in_issue,real_name,gender,"
            "birth,origin,publisher",
            "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,"
            "first_appeared_in_issue,real_name,gender,birth,origin,character_friends,character_enemies,"
            "teams,team_enemies,team_friends,publisher,creators,powers",
        ),
        Endpoint(
            "comicvine_concepts",
            "concepts",
            "id,api_detail_url,site_detail_url,name,aliases,deck,image,first_appeared_in_issue,start_year",
            "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,"
            "first_appeared_in_issue,start_year",
        ),
        Endpoint(
            "comicvine_issues",
            "issues",
            "id,api_detail_url,site_detail_url,name,aliases,deck,image,issue_number,cover_date," "store_date,volume",
            "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,issue_number,"
            "cover_date,store_date,character_credits,character_died_in,concept_credits,location_credits,"
            "object_credits,person_credits,story_arc_credits,team_credits,team_disbanded_in,volume",
        ),
        Endpoint(
            "comicvine_locations",
            "locations",
            "id,api_detail_url,site_detail_url,name,aliases,deck,image,first_appeared_in_issue,start_year",
            "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,"
            "first_appeared_in_issue,start_year",
        ),
        Endpoint(
            "comicvine_objects",
            "objects",
            "id,api_detail_url,site_detail_url,name,aliases,deck,image," "first_appeared_in_issue,start_year",
            "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,"
            "first_appeared_in_issue,start_year",
        ),
        Endpoint(
            "comicvine_people",
            "people",
            "id,api_detail_url,site_detail_url,name,aliases,deck,image,birth,country,death,hometown",
            "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,birth,country,death," "hometown",
        ),
        Endpoint(
            "comicvine_powers",
            "powers",
            "id,api_detail_url,site_detail_url,name,aliases",
            "id,api_detail_url,site_detail_url,name,aliases,description",
        ),
        Endpoint(
            "comicvine_publishers",
            "publishers",
            "id,api_detail_url,site_detail_url,name,aliases,deck,image",
            "id,api_detail_url,site_detail_url,name,aliases,deck,description,image",
        ),
        Endpoint(
            "comicvine_story_arcs",
            "story_arcs",
            "id,api_detail_url,site_detail_url,name,aliases,deck,image,first_appeared_in_issue,publisher",
            "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,first_appeared_in_issue,publisher",
        ),
        Endpoint(
            "comicvine_teams",
            "teams",
            "id,api_detail_url,site_detail_url,name,aliases,deck,image,first_appeared_in_issue,publisher",
            "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,"
            "first_appeared_in_issue,publisher",
        ),
        Endpoint(
            "comicvine_volumes",
            "volumes",
            "id,api_detail_url,site_detail_url,name,aliases,deck,image,first_issue,publisher,last_issue," "start_year",
            "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,first_issue,"
            "publisher,last_issue,start_year",
        ),
    )
    LIST_URL_PATTERN = (
        "https://comicvine.gamespot.com/api/{endpoint}/?"
        "format=json&"
        "field_list={list_url_fields}&"
        "sort=id:asc&"
        "offset={offset}&"
        "limit={limit}&"
        "api_key={api_key}"
    )

    LIMIT = 100

    name = "full_spider"

    def __init__(self, incremental="Y", api_keys=None, filters=None, skip_existing="N", mongo_url=None, **kwargs):
        self.logger.info("incremental: " + incremental)
        self.logger.info("skip_existing: " + skip_existing)
        if filters is None:
            filters = {}
        if not self.LIST_URL_PATTERN:
            raise SpiderImplementationError(f"Class `{self.__class__}` should override `LIST_URL_PATTERN`")
        super().__init__(**kwargs)
        self.api_keys = api_keys
        self.filters = filters
        self.incremental = incremental
        self.skip_existing = skip_existing
        self.mongo_url = mongo_url

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.api_keys = spider.api_keys or spider.settings.get("API_KEYS")
        spider.mongo_url = spider.mongo_url or spider.settings.get("MONGO_URL")
        mongo_connection = Connect.get_connection(spider.mongo_url)
        spider.logger.info("Spider name: " + spider.name)
        spider.logger.info("API_KEY: " + str(spider.api_keys))
        spider.logger.info("MONGO_URL: " + spider.mongo_url)
        mongo_db = mongo_connection.get_default_database()

        if spider.incremental == "Y":
            spider_info = mongo_db.spider_info.find_one({"name": spider.name})
            spider.logger.info("Spider info: " + str(spider_info))
            if spider_info:
                start_date = str(
                    spider_info.get("last_run_dttm", datetime.datetime.min + datetime.timedelta(days=1))
                    - datetime.timedelta(days=1)
                )
                end_date = str(datetime.datetime.max)
                spider.filters["date_last_updated"] = f"{start_date}|{end_date}"

        mongo_db.spider_info.update(
            {"name": spider.name}, {"last_run_dttm": datetime.datetime.now(), "name": spider.name}, upsert=True
        )
        mongo_connection.close()

        return spider

    def start_requests(self):
        for endpoint in self.ENDPOINTS:
            url = self.construct_list_url(endpoint.endpoint, endpoint.list_url_fields, 0)
            yield EndpointRequest(url=url, endpoint=endpoint, callback=self.parse_list)

    def construct_list_url(self, endpoint, list_url_fields, offset):
        url = self.LIST_URL_PATTERN.format(
            **{
                "api_key": random.choice(self.api_keys),
                "limit": self.LIMIT,
                "offset": offset,
                "endpoint": endpoint,
                "list_url_fields": list_url_fields,
            }
        )
        filter_str = ",".join([f"{k}:{v}" for k, v in self.filters.items()])
        url += "&filter=" + filter_str
        self.logger.info("List url: " + url)
        return url

    def construct_detail_url(self, url, filed_list=None):
        url += "?api_key=" + random.choice(self.api_keys)
        url += "&format=json"
        if filed_list:
            url += "&field_list=" + filed_list
        return url

    def parse(self, response):
        pass

    def parse_list(self, response):
        # Parsing json
        json_res = json.loads(response.body)
        endpoint = response.request.endpoint

        mongo_connection = Connect.get_connection(self.settings.get("MONGO_URL"))
        mongo_db = mongo_connection.get_default_database()
        collection = mongo_db[endpoint.collection]

        # Follow to next list page
        offset = json_res["offset"]
        number_of_total_results = json_res["number_of_total_results"]
        number_of_page_results = json_res["number_of_page_results"]

        if offset + number_of_page_results < number_of_total_results:
            next_page = self.construct_list_url(
                endpoint.endpoint, endpoint.list_url_fields, offset + number_of_page_results
            )
            yield EndpointRequest(url=next_page, endpoint=endpoint, callback=self.parse_list, priority=1)

        # Follow to detail pages
        for entry in json_res.get("results", []):
            if (
                self.skip_existing == "N"
                or collection.count_documents({"id": int(entry["id"]), "crawl_source": "detail"}) == 0
            ):
                entry["crawl_date"] = datetime.datetime.now()
                entry["crawl_source"] = "list"
                item = {"_collection": response.request.endpoint.collection, "item": entry}
                yield item
                detail_url = self.construct_detail_url(entry["api_detail_url"], endpoint.detail_url_fields)
                yield EndpointRequest(url=detail_url, endpoint=endpoint, callback=self.parse_detail)
            else:
                self.logger.info(f"Skip existing: {entry['api_detail_url']}")
                yield {
                    "id": entry["id"],
                    "api_detail_url": entry["api_detail_url"],
                    "name": entry.get("name"),
                    "skip": True,
                }

        mongo_connection.close()

    def parse_detail(self, response):
        entry = json.loads(response.body).get("results", {})
        entry["crawl_date"] = datetime.datetime.now()
        entry["crawl_source"] = "detail"
        item = {"_collection": response.request.endpoint.collection, "item": entry}
        yield item
