from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin


class TestObjectsApiUrls(CountAPIUrlTestMixin):
    base_url = "objects"
    base_name = "object"
