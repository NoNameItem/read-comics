import pytest
from django.db.models import Count
from utils.utils import flatten_dict

from read_comics.concepts.models import Concept

pytestmark = pytest.mark.django_db


class TestConceptsCount:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client, concepts_no_issues, concepts_with_issues) -> None:
        response = api_client().get("/api/concepts/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(concepts_with_issues)

    @staticmethod
    def test_count_all(api_client, concepts_no_issues, concepts_with_issues) -> None:
        response = api_client().get("/api/concepts/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(concepts_with_issues) + len(concepts_no_issues)


class TestConceptsList:
    list_keys = {"slug", "image", "name", "short_description", "issues_count", "volumes_count"}

    def test_no_show_all(self, api_client, concepts_no_issues, concepts_with_issues) -> None:
        response = api_client().get("/api/concepts/")

        assert response.status_code == 200
        assert response.data["count"] == len(concepts_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_show_all(self, api_client, concepts_no_issues, concepts_with_issues) -> None:
        response = api_client().get("/api/concepts/?show-all=yes")

        assert response.status_code == 200
        assert response.data["count"] == len(concepts_no_issues) + len(concepts_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_data(api_client, concept_with_issues: Concept):
        response = api_client().get("/api/concepts/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == concept_with_issues.slug
        assert response_data["name"] == concept_with_issues.name
        assert response_data["short_description"] == concept_with_issues.short_description
        assert response_data["issues_count"] == concept_with_issues.issues.count()
        assert (
            response_data["volumes_count"]
            == concept_with_issues.issues.aggregate(v=Count("volume", distinct=True))["v"]
        )
