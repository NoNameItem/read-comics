import datetime
import json

import scrapy

from ..mongo_connection import Connect


class SpiderImplementationError(Exception):
    pass


class BaseSpider(scrapy.Spider):
    # LIST_URL_PATTERN should contain 3 placeholders: limit, offset and api_key and should not contain filter parameter
    LIST_URL_PATTERN = None
    DETAIL_FIELD_LIST = None
    LIMIT = 100

    def __init__(self, incremental="N", api_key=None, filters=None, skip_existing="N", mongo_url=None, **kwargs):
        self.logger.info("incremental: " + incremental)
        self.logger.info("skip_existing: " + skip_existing)
        if filters is None:
            filters = {}
        if not self.LIST_URL_PATTERN:
            raise SpiderImplementationError(f"Class `{self.__class__}` should override `LIST_URL_PATTERN`")
        super().__init__(**kwargs)
        self.api_key = api_key
        self.filters = filters
        self.incremental = incremental
        self.skip_existing = skip_existing
        self.mongo_url = mongo_url

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.api_key = spider.api_key or spider.settings.get("API_KEY")
        spider.mongo_url = spider.mongo_url or spider.settings.get("MONGO_URL")
        mongo_connection = Connect.get_connection(spider.mongo_url)
        spider.logger.info("Spider name: " + spider.name)
        spider.logger.info("API_KEY: " + spider.api_key)
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
        url = self.construct_list_url(0)

        yield scrapy.Request(url=url, callback=self.parse_list)

    def construct_list_url(self, offset):
        url = self.LIST_URL_PATTERN.format(**{"api_key": self.api_key, "limit": self.LIMIT, "offset": offset})
        filter_str = ",".join([f"{k}:{v}" for k, v in self.filters.items()])
        url += "&filter=" + filter_str
        self.logger.info("List url: " + url)
        return url

    def construct_detail_url(self, url):
        url += "?api_key=" + self.api_key
        url += "&format=json"
        if self.DETAIL_FIELD_LIST:
            url += "&field_list=" + self.DETAIL_FIELD_LIST
        self.logger.info("Detail url: " + url)
        return url

    def parse(self, response):
        pass  # Implementation not needed

    def parse_list(self, response):
        # Parsing json
        json_res = json.loads(response.body)

        mongo_connection = Connect.get_connection(self.settings.get("MONGO_URL"))
        mongo_db = mongo_connection.get_default_database()
        collection = mongo_db[self.name]

        # Follow to detail pages
        for entry in json_res.get("results", []):
            if (
                self.skip_existing == "N"
                or collection.count_documents({"id": int(entry["id"]), "crawl_source": "detail"}) == 0
            ):
                entry["crawl_date"] = datetime.datetime.now()
                entry["crawl_source"] = "list"
                yield entry
                detail_url = self.construct_detail_url(entry["api_detail_url"])
                yield scrapy.Request(url=detail_url, callback=self.parse_detail)
            else:
                self.logger.info(f"Skip existing: {entry['api_detail_url']}")
                yield {
                    "id": entry["id"],
                    "api_detail_url": entry["api_detail_url"],
                    "name": entry.get("name"),
                    "skip": True,
                }

        mongo_connection.close()

        # Follow to next list page
        offset = json_res["offset"]
        number_of_total_results = json_res["number_of_total_results"]
        number_of_page_results = json_res["number_of_page_results"]

        if offset + number_of_page_results < number_of_total_results:
            next_page = self.construct_list_url(offset + number_of_page_results)
            yield scrapy.Request(url=next_page, callback=self.parse_list)

    def parse_detail(self, response):
        item = json.loads(response.body).get("results", {})
        item["crawl_date"] = datetime.datetime.now()
        item["crawl_source"] = "detail"
        return item
