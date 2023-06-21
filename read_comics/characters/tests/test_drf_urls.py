import pytest
from django.urls import resolve, reverse


class TestCharactersApiUrls:
    @staticmethod
    def test_list() -> None:
        assert reverse("api:character-list") == "/api/characters/"
        assert resolve("/api/characters/").view_name == "api:character-list"

    @staticmethod
    @pytest.mark.django_db
    def test_detail(character_with_issues) -> None:
        assert (
            reverse("api:character-detail", kwargs={"slug": character_with_issues.slug})
            == f"/api/characters/{character_with_issues.slug}/"
        )
        assert resolve(f"/api/characters/{character_with_issues.slug}/").view_name == "api:character-detail"

    @staticmethod
    @pytest.mark.django_db
    def test_technical_info(character_with_issues) -> None:
        assert (
            reverse("api:character-technical-info", kwargs={"slug": character_with_issues.slug})
            == f"/api/characters/{character_with_issues.slug}/technical-info/"
        )
        assert (
            resolve(f"/api/characters/{character_with_issues.slug}/technical-info/").view_name
            == "api:character-technical-info"
        )

    @staticmethod
    def test_count() -> None:
        assert reverse("api:character-count") == "/api/characters/count/"
        assert resolve("/api/characters/count/").view_name == "api:character-count"
