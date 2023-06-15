import pytest
from django.urls import resolve, reverse


class TestConceptsApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:concept-count") == "/api/concepts/count/"
        assert resolve("/api/concepts/count/").view_name == "api:concept-count"

    @staticmethod
    def test_list() -> None:
        assert reverse("api:concept-list") == "/api/concepts/"
        assert resolve("/api/concepts/").view_name == "api:concept-list"

    @staticmethod
    @pytest.mark.django_db
    def test_detail(concept_with_issues) -> None:
        assert (
            reverse("api:concept-detail", kwargs={"slug": concept_with_issues.slug})
            == f"/api/concepts/{concept_with_issues.slug}/"
        )
        assert resolve(f"/api/concepts/{concept_with_issues.slug}/").view_name == "api:concept-detail"

    @staticmethod
    @pytest.mark.django_db
    def test_technical_info(concept_with_issues) -> None:
        assert (
            reverse("api:concept-technical-info", kwargs={"slug": concept_with_issues.slug})
            == f"/api/concepts/{concept_with_issues.slug}/technical-info/"
        )
        assert (
            resolve(f"/api/concepts/{concept_with_issues.slug}/technical-info/").view_name
            == "api:concept-technical-info"
        )
