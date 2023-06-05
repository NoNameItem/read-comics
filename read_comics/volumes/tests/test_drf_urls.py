from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin, StartedAPIUrlTestMixin


class TestVolumesApiUrls(CountAPIUrlTestMixin, StartedAPIUrlTestMixin):
    base_url = "volumes"
    base_name = "volume"
