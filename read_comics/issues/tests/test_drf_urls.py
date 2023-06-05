from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin


class TestIssuesApiUrls(CountAPIUrlTestMixin):
    base_url = "issues"
    base_name = "issue"
