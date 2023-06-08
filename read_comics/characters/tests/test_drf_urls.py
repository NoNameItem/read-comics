from django.urls import resolve, reverse


class TestCharactersApiUrls:
    base_url = "characters"
    base_name = "character"

    @staticmethod
    def test_list() -> None:
        assert reverse("api:character-list") == "/api/characters/"
        assert resolve("/api/characters/").view_name == "api:character-list"

    @staticmethod
    def test_count() -> None:
        assert reverse("api:character-count") == "/api/characters/count/"
        assert resolve("/api/characters/count/").view_name == "api:character-count"
