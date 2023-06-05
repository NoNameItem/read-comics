from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin


class TestLocationsApiUrls(CountAPIUrlTestMixin):
    base_url = "locations"
    base_name = "location"
