from django.urls import resolve, reverse


class TestStoryArcsApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:story-arc-count") == "/api/story-arcs/count/"
        assert resolve("/api/story-arcs/count/").view_name == "api:story-arc-count"

    @staticmethod
    def test_list() -> None:
        assert reverse("api:story-arc-list") == "/api/story-arcs/"
        assert resolve("/api/story-arcs/").view_name == "api:story-arc-list"

    @staticmethod
    def test_started() -> None:
        assert reverse("api:story-arc-started") == "/api/story-arcs/started/"
        assert resolve("/api/story-arcs/started/").view_name == "api:story-arc-started"
