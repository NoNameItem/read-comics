from .mongo_connection import Connect


class MongoPipeline:
    def __init__(self, mongo_url):
        self._mongo_url = mongo_url
        self._mongo_client = None
        self._mongo_collection = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get("MONGO_URL")
        )

    def process_item(self, item, spider):
        self._mongo_client = Connect.get_connection(self._mongo_url)
        if item.get("_collection"):
            self._mongo_collection = self._mongo_client.get_default_database()[item.get("_collection")]
            item = item["item"]
        else:
            self._mongo_collection = self._mongo_client.get_default_database()[spider.name]

        if not item.get("skip"):
            self._mongo_collection.update_one({"id": item["id"]}, {"$set": dict(item)}, upsert=True)
            self._mongo_client.close()
            return {"id": item["id"], "api_detail_url": item["api_detail_url"], "crawl_date": item["crawl_date"],
                    "name": item.get("name")}
        else:
            self._mongo_client.close()
            return item
