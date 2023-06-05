from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin


class TestConceptsApiUrls(CountAPIUrlTestMixin):
    base_url = "concepts"
    base_name = "concept"
