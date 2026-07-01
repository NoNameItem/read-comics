# Docs: [[docs/backend/concepts/testing/test_e2e.md]]
import sys

import pytest
from django.db.models import Count
from django.utils import timezone
from rest_framework.test import APIClient

from read_comics.concepts.models import Concept
from read_comics.utils.utils import flatten_dict

pytestmark = pytest.mark.django_db


class TestConceptsCount:
    # Count tests
    ##########################

    @staticmethod
    def test_count(
        api_client: APIClient, concepts_no_issues: list[Concept], concepts_with_issues: list[Concept]
    ) -> None:
        response = api_client.get("/api/concepts/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(concepts_with_issues)

    @staticmethod
    def test_count_all(
        api_client: APIClient, concepts_no_issues: list[Concept], concepts_with_issues: list[Concept]
    ) -> None:
        response = api_client.get("/api/concepts/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(concepts_with_issues) + len(concepts_no_issues)


class TestConceptsList:
    list_keys = {"slug", "image", "name", "short_description", "issues_count", "volumes_count"}

    def test_no_show_all(
        self, api_client: APIClient, concepts_no_issues: list[Concept], concepts_with_issues: list[Concept]
    ) -> None:
        response = api_client.get("/api/concepts/")

        assert response.status_code == 200
        assert response.data["count"] == len(concepts_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_show_all(
        self, api_client: APIClient, concepts_no_issues: list[Concept], concepts_with_issues: list[Concept]
    ) -> None:
        response = api_client.get("/api/concepts/?show-all=yes")

        assert response.status_code == 200
        assert response.data["count"] == len(concepts_no_issues) + len(concepts_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_data(api_client: APIClient, concept_with_issues: Concept):
        response = api_client.get("/api/concepts/")

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

    @staticmethod
    def test_default_ordering_by_name(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        response = api_client.get("/api/concepts/")

        assert response.status_code == 200
        assert response.data["count"] == len(concepts_with_issues)

        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_ascending(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        response = api_client.get("/api/concepts/?ordering=name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_descending(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        response = api_client.get("/api/concepts/?ordering=-name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names, reverse=True)

    @staticmethod
    def test_ordering_by_issues_count_ascending(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        response = api_client.get("/api/concepts/?ordering=issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts)

    @staticmethod
    def test_ordering_by_issues_count_descending(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        response = api_client.get("/api/concepts/?ordering=-issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts, reverse=True)

    @staticmethod
    def test_ordering_by_volumes_count_ascending(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        response = api_client.get("/api/concepts/?ordering=volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts)

    @staticmethod
    def test_ordering_by_volumes_count_descending(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        response = api_client.get("/api/concepts/?ordering=-volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts, reverse=True)

    @staticmethod
    def test_invalid_ordering_field(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        """Test that invalid ordering field falls back to default ordering."""
        default_response = api_client.get("/api/concepts/")
        invalid_ordering_response = api_client.get("/api/concepts/?ordering=invalid_field")

        assert invalid_ordering_response.status_code == 200

        default_names = [item["name"] for item in default_response.data["results"]]
        invalid_ordering_names = [item["name"] for item in invalid_ordering_response.data["results"]]
        assert invalid_ordering_names == default_names

    @staticmethod
    def test_pagination_invalid_page(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        response = api_client.get("/api/concepts/?page=999")

        assert response.status_code == 404


class TestConceptDetail:
    @staticmethod
    def test_with_first_issue(api_client: APIClient, concept_with_issues: Concept) -> None:
        response = api_client.get(f"/api/concepts/{concept_with_issues.slug}/")

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
    def test_no_first_issue(api_client: APIClient, concept_no_issues: Concept) -> None:
        response = api_client.get(f"/api/concepts/{concept_no_issues.slug}/")

        assert response.status_code == 200

        assert response.data["first_issue_name"] == concept_no_issues.first_issue_name
        assert response.data["first_issue_slug"] is None
        assert response.data["download_size"] == "0\xa0bytes"

    @staticmethod
    def test_not_found(api_client: APIClient) -> None:
        response = api_client.get("/api/concepts/does-not-exist/")

        assert response.status_code == 404


class TestConceptTechnicalInfo:
    @staticmethod
    def test_no_auth(api_client: APIClient, concept_no_issues: Concept) -> None:
        response = api_client.get(f"/api/concepts/{concept_no_issues.slug}/technical-info/")

        assert response.status_code == 401

    @staticmethod
    def test_regular_user(authenticated_api_client: APIClient, concept_no_issues: Concept) -> None:
        response = authenticated_api_client.get(f"/api/concepts/{concept_no_issues.slug}/technical-info/")

        assert response.status_code == 403

    @staticmethod
    def test_staff(staff_api_client: APIClient, concept_no_issues: Concept) -> None:
        response = staff_api_client.get(f"/api/concepts/{concept_no_issues.slug}/technical-info/")

        assert response.status_code == 200

    @staticmethod
    @pytest.mark.skipif(sys.version_info < (3, 12), reason="requires Python 3.12 or later")
    def test_superuser(superuser_api_client: APIClient, concept_no_issues: Concept) -> None:
        response = superuser_api_client.get(f"/api/concepts/{concept_no_issues.slug}/technical-info/")

        assert response.status_code == 200

        assert response.data["id"] == concept_no_issues.id
        assert response.data["comicvine_id"] == concept_no_issues.comicvine_id
        assert response.data["comicvine_status"] == concept_no_issues.get_comicvine_status_display()
        assert (
            response.data["comicvine_last_match"]
            == timezone.localtime(concept_no_issues.comicvine_last_match).isoformat()
        )
        assert response.data["created_dt"] == timezone.localtime(concept_no_issues.created_dt).isoformat()
        assert response.data["modified_dt"] == timezone.localtime(concept_no_issues.modified_dt).isoformat()


# ============================================================================
# PARAMETRIZED, EDGE CASE, CONSISTENCY, HTTP METHOD & INTEGRATION TESTS
# ============================================================================


class TestConceptsParametrized:
    """Parametrized tests for sorting."""

    @pytest.mark.parametrize(
        "ordering,is_reverse",
        [
            ("name", False),
            ("-name", True),
            ("issues_count", False),
            ("-issues_count", True),
            ("volumes_count", False),
            ("-volumes_count", True),
        ],
    )
    def test_ordering_parametrized(
        self, api_client: APIClient, concepts_with_issues: list[Concept], ordering: str, is_reverse: bool
    ) -> None:
        response = api_client.get(f"/api/concepts/?ordering={ordering}")
        assert response.status_code == 200
        field = ordering.lstrip("-")
        values = [item[field] for item in response.data["results"]]
        assert values == sorted(values, reverse=is_reverse)


class TestConceptsEdgeCases:
    @staticmethod
    def test_pagination_boundary_first_page(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        response = api_client.get("/api/concepts/?page=1")
        assert response.status_code == 200
        assert "results" in response.data

    @staticmethod
    def test_pagination_boundary_zero_page(api_client: APIClient) -> None:
        response = api_client.get("/api/concepts/?page=0")
        assert response.status_code == 404

    @staticmethod
    def test_pagination_boundary_negative_page(api_client: APIClient) -> None:
        response = api_client.get("/api/concepts/?page=-1")
        assert response.status_code == 404

    @staticmethod
    def test_list_with_large_page_size(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        response = api_client.get("/api/concepts/?page_size=10000")
        assert response.status_code == 200
        assert response.data["count"] == len(concepts_with_issues)

    @staticmethod
    def test_response_structure_includes_all_pagination_fields(
        api_client: APIClient, concept_with_issues: Concept
    ) -> None:
        response = api_client.get("/api/concepts/")
        assert response.status_code == 200
        assert all(k in response.data for k in ["count", "next", "previous", "results"])


class TestConceptsConsistency:
    @staticmethod
    def test_list_detail_field_consistency(api_client: APIClient, concept_with_issues: Concept) -> None:
        list_response = api_client.get("/api/concepts/")
        detail_response = api_client.get(f"/api/concepts/{concept_with_issues.slug}/")
        assert list_response.status_code == 200 and detail_response.status_code == 200
        for key in list_response.data["results"][0].keys():
            if key not in ("issues_count", "volumes_count"):
                assert key in detail_response.data

    @staticmethod
    def test_count_vs_list_count_consistency(api_client: APIClient, concepts_with_issues: list[Concept]) -> None:
        list_response = api_client.get("/api/concepts/")
        count_response = api_client.get("/api/concepts/count/")
        assert list_response.data["count"] == count_response.data["count"]


class TestConceptsHTTPMethods:
    @staticmethod
    def test_list_endpoint_rejects_post(api_client: APIClient) -> None:
        response = api_client.post("/api/concepts/", {"name": "New"})
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_detail_endpoint_rejects_put(api_client: APIClient, concept_with_issues: Concept) -> None:
        response = api_client.put(f"/api/concepts/{concept_with_issues.slug}/", {"name": "Updated"})
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_response_content_type_is_json(api_client: APIClient) -> None:
        response = api_client.get("/api/concepts/")
        assert "application/json" in response.get("Content-Type", "")
