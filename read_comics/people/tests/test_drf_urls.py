from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin


class TestPeopleApiUrls(CountAPIUrlTestMixin):
    base_url = "people"
    base_name = "people"
