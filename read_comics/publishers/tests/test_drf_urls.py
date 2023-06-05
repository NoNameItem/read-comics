from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin


class TestPublishersApiUrls(CountAPIUrlTestMixin):
    base_url = "publishers"
    base_name = "publisher"
