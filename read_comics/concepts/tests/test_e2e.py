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


class TestConceptDetail:
    @staticmethod
    def test_with_first_issue(api_client, concept_with_issues: Concept):
        response = api_client().get(f"/api/concepts/{concept_with_issues.slug}/")

        assert response.status_code == 200

        assert response.data["slug"] == concept_with_issues.slug
        assert response.data["name"] == concept_with_issues.name
        assert response.data["aliases"] == concept_with_issues.get_aliases_list()
        assert response.data["start_year"] == concept_with_issues.start_year
        assert response.data["first_issue_name"] == (
            concept_with_issues.first_issue.display_name if concept_with_issues.first_issue is not None else None
        )
        assert response.data["first_issue_slug"] == (
            concept_with_issues.first_issue.slug if concept_with_issues.first_issue is not None else None
        )
        assert response.data["comicvine_url"] == concept_with_issues.comicvine_url
        assert response.data["short_description"] == concept_with_issues.short_description
        assert response.data["description"] == concept_with_issues.description
        assert response.data["download_size"] == concept_with_issues.download_size
        assert response.data["download_link"] == f"http://testserver{concept_with_issues.download_link}"

    @staticmethod
    def test_no_first_issue(api_client, concept_no_issues: Concept):
        response = api_client().get(f"/api/concepts/{concept_no_issues.slug}/")

        assert response.status_code == 200

        assert response.data["first_issue_name"] == concept_no_issues.first_issue_name
        assert response.data["first_issue_slug"] is None
        assert response.data["download_size"] == "0\xa0bytes"


class TestConceptTechnicalInfo:
    @staticmethod
    def test_no_auth(api_client, concept_no_issues: Concept):
        response = api_client().get(f"/api/concepts/{concept_no_issues.slug}/technical-info/")

        assert response.status_code == 401

    @staticmethod
    def test_regular_user(authenticated_api_client, concept_no_issues: Concept):
        response = authenticated_api_client.get(f"/api/concepts/{concept_no_issues.slug}/technical-info/")

        assert response.status_code == 403

    @staticmethod
    def test_staff(staff_api_client, concept_no_issues: Concept):
        response = staff_api_client.get(f"/api/concepts/{concept_no_issues.slug}/technical-info/")

        assert response.status_code == 200

    @staticmethod
    def test_superuser(superuser_api_client, concept_no_issues: Concept):
        response = superuser_api_client.get(f"/api/concepts/{concept_no_issues.slug}/technical-info/")

        assert response.status_code == 200

        assert response.data["id"] == concept_no_issues.id
        assert response.data["comicvine_id"] == concept_no_issues.comicvine_id
        assert response.data["comicvine_status"] == concept_no_issues.get_comicvine_status_display()
        assert response.data["comicvine_last_match"] == concept_no_issues.comicvine_last_match.strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        assert response.data["created_dt"] == concept_no_issues.created_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        assert response.data["modified_dt"] == concept_no_issues.modified_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
