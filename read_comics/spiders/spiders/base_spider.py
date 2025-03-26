import datetime
import json
import random

import scrapy
from django.utils import timezone

from ..mongo_connection import Connect


class SpiderImplementationError(Exception):
    pass


class BaseSpider(scrapy.Spider):
    # LIST_URL_PATTERN should contain 3 placeholders: limit, offset and api_key and should not contain filter parameter
    LIST_URL_PATTERN = None
    DETAIL_FIELD_LIST = None
    LIMIT = 50

    def __init__(self, incremental="N", api_keys=None, filters=None, skip_existing="N", mongo_url=None, **kwargs):
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
        self.max_offset = 0

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
                    spider_info.get("last_run_dttm", datetime.datetime.min + datetime.timedelta(hours=1))
                    - datetime.timedelta(hours=1)
                )
                end_date = str(datetime.datetime.max)
                spider.filters["date_last_updated"] = f"{start_date}|{end_date}"

        mongo_db.spider_info.update(
            {"name": spider.name}, {"last_run_dttm": timezone.now(), "name": spider.name}, upsert=True
        )
        mongo_connection.close()

        return spider

    def start_requests(self):
        url = self.construct_list_url(0)
        yield scrapy.Request(url=url, callback=self.parse_list)

    def construct_list_url(self, offset):
        url = self.LIST_URL_PATTERN.format(
            **{"api_key": random.choice(self.api_keys), "limit": self.LIMIT, "offset": offset}
        )
        filter_str = ",".join([f"{k}:{v}" for k, v in self.filters.items()])
        url += "&filter=" + filter_str
        return url

    def construct_detail_url(self, url):
        url += "?api_key=" + random.choice(self.api_keys)
        url += "&format=json"
        if self.DETAIL_FIELD_LIST:
            url += "&field_list=" + self.DETAIL_FIELD_LIST
        return url

    def parse(self, response):
        pass  # Implementation not needed

    def parse_list(self, response):
        # Parsing json
        json_res = json.loads(response.body)

        mongo_connection = Connect.get_connection(self.settings.get("MONGO_URL"))
        mongo_db = mongo_connection.get_default_database()
        collection = mongo_db[self.name]

        # Follow to next list pages
        number_of_total_results = json_res["number_of_total_results"]

        list_urls = []
        while self.max_offset + self.LIMIT < number_of_total_results:
            self.max_offset += self.LIMIT
            list_urls.append(self.construct_list_url(self.max_offset))

        for url in list_urls:
            yield scrapy.Request(url=url, callback=self.parse_list, priority=5)

        # Follow to detail pages
        for entry in json_res.get("results", []):
            if (
                self.skip_existing == "N"
                or collection.count_documents({"id": int(entry["id"]), "crawl_source": "detail"}) == 0
            ):
                if collection.count_documents({"id": int(entry["id"]), "crawl_source": "detail"}) == 0:
                    # Updating from list only if there is no version with info from detail
                    entry["crawl_date"] = timezone.now()
                    entry["crawl_source"] = "list"
                    yield entry
                detail_url = self.construct_detail_url(entry["api_detail_url"])
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail,
                    priority=1,
                    meta={"check_comicvine_id": entry["id"]},
                )
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
        item = json.loads(response.body).get("results", {})
        item["crawl_date"] = timezone.now()
        item["crawl_source"] = "detail"
        return item
