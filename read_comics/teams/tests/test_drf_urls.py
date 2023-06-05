from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin


class TestTeamsApiUrls(CountAPIUrlTestMixin):
    base_url = "teams"
    base_name = "team"
