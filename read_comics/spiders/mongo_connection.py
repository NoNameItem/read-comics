from pymongo import MongoClient


class Connect:
    @staticmethod
    def get_connection(url):
        return MongoClient(url)
