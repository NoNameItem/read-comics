from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin


class TestMissingIssuesApiUrls(CountAPIUrlTestMixin):
    base_url = "missing-issues"
    base_name = "missing-issue"
