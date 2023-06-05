from utils.test_utils.api_urls_mixins import CountAPIUrlTestMixin, StartedAPIUrlTestMixin


class TestStoryArcsApiUrls(CountAPIUrlTestMixin, StartedAPIUrlTestMixin):
    base_url = "story-arcs"
    base_name = "story-arc"
