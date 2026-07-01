# Docs: [[docs/backend/spiders/infrastructure.md#mongo_connectionpy]]
from pymongo import MongoClient


class Connect:
    @staticmethod
    def get_connection(url):
        return MongoClient(url)
