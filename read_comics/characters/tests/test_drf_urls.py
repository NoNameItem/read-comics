from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin


class TestCharactersApiUrls(CountAPIUrlTestMixin):
    base_url = "characters"
    base_name = "character"
