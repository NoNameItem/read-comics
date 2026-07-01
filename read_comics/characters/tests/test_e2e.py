# Docs: [[docs/backend/characters/testing/test_e2e.md]]
import sys
from datetime import date

import pytest
from django.db.models import Count
from django.utils import timezone
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from ..models import Character

pytestmark = pytest.mark.django_db


class TestCharactersCount:
    @staticmethod
    def test_no_show_all(
        api_client: APIClient, characters_no_issues: list[Character], characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues)

    @staticmethod
    def test_show_all(
        api_client: APIClient, characters_no_issues: list[Character], characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues) + len(characters_no_issues)


class TestCharactersList:
    list_keys = {
        "slug",
        "image",
        "publisher__name",
        "publisher__image",
        "publisher__slug",
        "name",
        "short_description",
        "issues_count",
        "volumes_count",
    }

    def test_no_show_all(
        self, api_client: APIClient, characters_no_issues: list[Character], characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/")

        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_show_all(
        self, api_client: APIClient, characters_no_issues: list[Character], characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/?show-all=yes")

        assert response.status_code == 200
        assert response.data["count"] == len(characters_no_issues) + len(characters_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_data(api_client: APIClient, character_with_issues: Character) -> None:
        response = api_client.get("/api/characters/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == character_with_issues.slug
        assert response_data["name"] == character_with_issues.name
        assert response_data["publisher"]["name"] == (
            character_with_issues.publisher.name if character_with_issues.publisher else None
        )
        assert response_data["publisher"]["slug"] == (
            character_with_issues.publisher.slug if character_with_issues.publisher else None
        )
        assert response_data["short_description"] == character_with_issues.short_description
        assert response_data["issues_count"] == character_with_issues.issues.count()
        assert (
            response_data["volumes_count"]
            == character_with_issues.issues.aggregate(v=Count("volume", distinct=True))["v"]
        )

    @staticmethod
    def test_default_ordering_by_name(api_client: APIClient, characters_with_issues: list[Character]) -> None:
        response = api_client.get("/api/characters/")

        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues)

        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_ascending(api_client: APIClient, characters_with_issues: list[Character]) -> None:
        response = api_client.get("/api/characters/?ordering=name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_descending(api_client: APIClient, characters_with_issues: list[Character]) -> None:
        response = api_client.get("/api/characters/?ordering=-name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names, reverse=True)

    @staticmethod
    def test_ordering_by_issues_count_ascending(api_client: APIClient, characters_with_issues: list[Character]) -> None:
        response = api_client.get("/api/characters/?ordering=issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts)

    @staticmethod
    def test_ordering_by_issues_count_descending(
        api_client: APIClient, characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/?ordering=-issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts, reverse=True)

    @staticmethod
    def test_ordering_by_volumes_count_ascending(
        api_client: APIClient, characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/?ordering=volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts)

    @staticmethod
    def test_invalid_ordering_field(api_client: APIClient, characters_with_issues: list[Character]) -> None:
        """Test that invalid ordering field falls back to default ordering."""
        default_response = api_client.get("/api/characters/")
        invalid_ordering_response = api_client.get("/api/characters/?ordering=invalid_field")

        assert invalid_ordering_response.status_code == 200

        default_names = [item["name"] for item in default_response.data["results"]]
        invalid_ordering_names = [item["name"] for item in invalid_ordering_response.data["results"]]
        assert invalid_ordering_names == default_names

    @staticmethod
    def test_pagination_invalid_page(api_client: APIClient, characters_with_issues: list[Character]) -> None:
        response = api_client.get("/api/characters/?page=999")

        assert response.status_code == 404


class TestCharacterDetail:
    @staticmethod
    def test_with_first_issue(api_client: APIClient, character_with_issues: Character) -> None:
        response = api_client.get(f"/api/characters/{character_with_issues.slug}/")

        assert response.status_code == 200

        assert response.data["slug"] == character_with_issues.slug
        assert response.data["name"] == character_with_issues.name
        assert response.data["real_name"] == character_with_issues.real_name
        assert response.data["publisher"]["name"] == (
            character_with_issues.publisher.name if character_with_issues.publisher is not None else None
        )
        assert response.data["publisher"]["slug"] == (
            character_with_issues.publisher.slug if character_with_issues.publisher is not None else None
        )
        assert response.data["aliases"] == character_with_issues.get_aliases_list()
        assert date.fromisoformat(response.data["birth"]) == character_with_issues.birth
        assert response.data["gender"] == character_with_issues.get_gender_display()
        assert set(response.data["powers"]) == set(map(lambda x: x.name, character_with_issues.powers.all()))
        assert response.data["first_issue_name"] == (
            character_with_issues.first_issue.display_name if character_with_issues.first_issue is not None else None
        )
        assert response.data["first_issue_slug"] == (
            character_with_issues.first_issue.slug if character_with_issues.first_issue is not None else None
        )
        assert response.data["comicvine_url"] == character_with_issues.comicvine_url
        assert response.data["short_description"] == character_with_issues.short_description
        assert response.data["description"] == character_with_issues.description
        assert response.data["download_size"] == character_with_issues.download_size
        assert response.data["download_link"] == f"http://testserver{character_with_issues.download_link}"

    @staticmethod
    def test_no_first_issue(api_client: APIClient, character_no_issues: Character) -> None:
        response = api_client.get(f"/api/characters/{character_no_issues.slug}/")

        assert response.status_code == 200

        assert response.data["first_issue_name"] == character_no_issues.first_issue_name
        assert response.data["first_issue_slug"] is None
        assert response.data["download_size"] == "0\xa0bytes"

    @staticmethod
    def test_not_found(api_client: APIClient) -> None:
        response = api_client.get("/api/characters/does-not-exist/")

        assert response.status_code == 404


class TestCharacterTechnicalInfo:
    @staticmethod
    def test_no_auth(api_client: APIClient, character_no_issues: Character) -> None:
        response = api_client.get(f"/api/characters/{character_no_issues.slug}/technical-info/")

        assert response.status_code == 401

    @staticmethod
    def test_regular_user(authenticated_api_client: APIClient, character_no_issues: Character) -> None:
        response = authenticated_api_client.get(f"/api/characters/{character_no_issues.slug}/technical-info/")

        assert response.status_code == 403

    @staticmethod
    def test_staff(staff_api_client: APIClient, character_no_issues: Character) -> None:
        response = staff_api_client.get(f"/api/characters/{character_no_issues.slug}/technical-info/")

        assert response.status_code == 200

    @staticmethod
    @pytest.mark.skipif(sys.version_info < (3, 12), reason="requires Python 3.12 or later")
    def test_superuser(superuser_api_client: APIClient, character_no_issues: Character) -> None:
        response = superuser_api_client.get(f"/api/characters/{character_no_issues.slug}/technical-info/")

        assert response.status_code == 200

        assert response.data["id"] == character_no_issues.id
        assert response.data["comicvine_id"] == character_no_issues.comicvine_id
        assert response.data["comicvine_status"] == character_no_issues.get_comicvine_status_display()
        assert (
            response.data["comicvine_last_match"]
            == timezone.localtime(character_no_issues.comicvine_last_match).isoformat()
        )
        assert response.data["created_dt"] == timezone.localtime(character_no_issues.created_dt).isoformat()
        assert response.data["modified_dt"] == timezone.localtime(character_no_issues.modified_dt).isoformat()

    @staticmethod
    def test_ordering_by_volumes_count_descending(
        api_client: APIClient, characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/?ordering=-volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts, reverse=True)


# ============================================================================
# PARAMETRIZED TESTS - Reduce duplication for sorting/filtering
# ============================================================================


class TestCharactersParametrized:
    """Parametrized tests for sorting to reduce code duplication."""

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
        self, api_client: APIClient, characters_with_issues: list[Character], ordering: str, is_reverse: bool
    ) -> None:
        """Test sorting by different fields in both directions."""
        response = api_client.get(f"/api/characters/?ordering={ordering}")

        assert response.status_code == 200
        field = ordering.lstrip("-")

        if field == "name":
            values = [item[field] for item in response.data["results"]]
            assert values == sorted(values, reverse=is_reverse)
        else:
            values = [item[field] for item in response.data["results"]]
            assert values == sorted(values, reverse=is_reverse)


# ============================================================================
# EDGE CASE TESTS
# ============================================================================


class TestCharactersEdgeCases:
    """Edge case and boundary condition tests."""

    @staticmethod
    def test_pagination_boundary_first_page(api_client: APIClient, characters_with_issues: list[Character]) -> None:
        """Test that page=1 returns valid results."""
        response = api_client.get("/api/characters/?page=1")
        assert response.status_code == 200
        assert "results" in response.data

    @staticmethod
    def test_pagination_boundary_zero_page(api_client: APIClient) -> None:
        """Test that page=0 returns 404."""
        response = api_client.get("/api/characters/?page=0")
        assert response.status_code == 404

    @staticmethod
    def test_pagination_boundary_negative_page(api_client: APIClient) -> None:
        """Test that negative page returns 404."""
        response = api_client.get("/api/characters/?page=-1")
        assert response.status_code == 404

    @staticmethod
    def test_list_with_large_page_size(api_client: APIClient, characters_with_issues: list[Character]) -> None:
        """Test that very large page_size works."""
        response = api_client.get("/api/characters/?page_size=10000")
        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues)

    @staticmethod
    def test_list_with_zero_page_size(api_client: APIClient) -> None:
        """Test that page_size=0 is handled."""
        response = api_client.get("/api/characters/?page_size=0")
        # Should either return error or handle gracefully
        assert response.status_code in [200, 400, 404]

    @staticmethod
    def test_response_structure_includes_all_pagination_fields(
        api_client: APIClient, character_with_issues: Character
    ) -> None:
        """Test that list response includes count, next, previous, results."""
        response = api_client.get("/api/characters/")
        assert response.status_code == 200
        assert "count" in response.data
        assert "next" in response.data
        assert "previous" in response.data
        assert "results" in response.data

    @staticmethod
    def test_list_response_structure_validation(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that response structure matches expected format."""
        response = api_client.get("/api/characters/")
        assert response.status_code == 200
        assert isinstance(response.data["count"], int)
        assert isinstance(response.data["results"], list)
        assert isinstance(response.data["results"][0], dict)


# ============================================================================
# CONSISTENCY TESTS - List vs Detail, List vs Count
# ============================================================================


class TestCharactersConsistency:
    """Tests to verify data consistency across endpoints."""

    @staticmethod
    def test_list_detail_field_consistency(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that fields in list response match fields in detail response."""
        list_response = api_client.get("/api/characters/")
        detail_response = api_client.get(f"/api/characters/{character_with_issues.slug}/")

        assert list_response.status_code == 200
        assert detail_response.status_code == 200

        list_item = list_response.data["results"][0]
        detail_item = detail_response.data

        # All list fields should exist in detail
        for key in list_item.keys():
            if key not in ("issues_count", "volumes_count"):
                assert key in detail_item, f"Field '{key}' in list but not in detail"

    @staticmethod
    def test_list_detail_value_consistency(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that values in list match values in detail for common fields."""
        list_response = api_client.get("/api/characters/")
        detail_response = api_client.get(f"/api/characters/{character_with_issues.slug}/")

        list_item = list_response.data["results"][0]
        detail_item = detail_response.data

        # Check that simple fields match
        assert list_item["slug"] == detail_item["slug"]
        assert list_item["name"] == detail_item["name"]
        assert list_item["short_description"] == detail_item["short_description"]

    @staticmethod
    def test_count_vs_list_count_consistency(
        api_client: APIClient, characters_with_issues: list[Character], characters_no_issues: list[Character]
    ) -> None:
        """Test that count endpoint matches list endpoint count."""
        list_response = api_client.get("/api/characters/")
        count_response = api_client.get("/api/characters/count/")

        assert list_response.status_code == 200
        assert count_response.status_code == 200
        assert list_response.data["count"] == count_response.data["count"]

    @staticmethod
    def test_count_vs_list_with_show_all_consistency(
        api_client: APIClient, characters_with_issues: list[Character], characters_no_issues: list[Character]
    ) -> None:
        """Test that show-all filter is consistent between list and count."""
        list_response = api_client.get("/api/characters/?show-all=yes")
        count_response = api_client.get("/api/characters/count/?show-all=yes")

        assert list_response.status_code == 200
        assert count_response.status_code == 200
        assert list_response.data["count"] == count_response.data["count"]

    @staticmethod
    def test_detail_response_has_all_expected_fields(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that detail response has all expected fields."""
        response = api_client.get(f"/api/characters/{character_with_issues.slug}/")

        assert response.status_code == 200
        expected_fields = {
            "slug",
            "name",
            "real_name",
            "birth",
            "gender",
            "short_description",
            "description",
            "comicvine_url",
            "download_size",
            "download_link",
        }
        actual_fields = set(response.data.keys())
        assert expected_fields.issubset(actual_fields)


# ============================================================================
# HTTP METHOD TESTS - Read-only endpoint validation
# ============================================================================


class TestCharactersHTTPMethods:
    """Test HTTP method restrictions on read-only endpoints."""

    @staticmethod
    def test_list_endpoint_rejects_post(api_client: APIClient) -> None:
        """Test that POST is not allowed on list endpoint."""
        response = api_client.post("/api/characters/", {"name": "New Character"})
        assert response.status_code in [405, 403, 400]  # Method Not Allowed or Forbidden

    @staticmethod
    def test_list_endpoint_rejects_put(api_client: APIClient) -> None:
        """Test that PUT is not allowed on list endpoint."""
        response = api_client.put("/api/characters/", {"name": "New Character"})
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_list_endpoint_rejects_patch(api_client: APIClient) -> None:
        """Test that PATCH is not allowed on list endpoint."""
        response = api_client.patch("/api/characters/", {"name": "New Character"})
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_list_endpoint_rejects_delete(api_client: APIClient) -> None:
        """Test that DELETE is not allowed on list endpoint."""
        response = api_client.delete("/api/characters/")
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_detail_endpoint_rejects_post(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that POST is not allowed on detail endpoint."""
        response = api_client.post(f"/api/characters/{character_with_issues.slug}/", {"name": "Updated"})
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_detail_endpoint_rejects_put(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that PUT is not allowed on detail endpoint."""
        response = api_client.put(f"/api/characters/{character_with_issues.slug}/", {"name": "Updated"})
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_detail_endpoint_rejects_patch(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that PATCH is not allowed on detail endpoint."""
        response = api_client.patch(f"/api/characters/{character_with_issues.slug}/", {"name": "Updated"})
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_detail_endpoint_rejects_delete(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that DELETE is not allowed on detail endpoint."""
        response = api_client.delete(f"/api/characters/{character_with_issues.slug}/")
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_count_endpoint_rejects_post(api_client: APIClient) -> None:
        """Test that POST is not allowed on count endpoint."""
        response = api_client.post("/api/characters/count/", {})
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_response_content_type_is_json(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that response Content-Type is JSON."""
        response = api_client.get("/api/characters/")
        assert "application/json" in response.get("Content-Type", "")


# ============================================================================
# CROSS-ENDPOINT INTEGRATION TESTS
# ============================================================================


class TestCharactersCrossEndpoint:
    """Integration tests across multiple endpoints."""

    @staticmethod
    def test_list_returns_correct_total_count(
        api_client: APIClient, characters_with_issues: list[Character], characters_no_issues: list[Character]
    ) -> None:
        """Test that list returns all items matching filter criteria."""
        response = api_client.get("/api/characters/")
        assert response.status_code == 200
        # Default behavior: show only items with issues
        assert response.data["count"] == len(characters_with_issues)

    @staticmethod
    def test_detail_slug_lookup_matches_list_slug(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that slug used in detail endpoint matches slug in list."""
        list_response = api_client.get("/api/characters/")
        assert list_response.status_code == 200

        list_slug = list_response.data["results"][0]["slug"]
        detail_response = api_client.get(f"/api/characters/{list_slug}/")
        assert detail_response.status_code == 200
        assert detail_response.data["slug"] == list_slug

    @staticmethod
    def test_filtering_consistency_across_endpoints(
        api_client: APIClient, characters_with_issues: list[Character], characters_no_issues: list[Character]
    ) -> None:
        """Test that filtering behavior is consistent across list and count."""
        # Default: show only with issues
        list_default = api_client.get("/api/characters/")
        count_default = api_client.get("/api/characters/count/")
        assert list_default.data["count"] == count_default.data["count"]

        # With show-all
        list_all = api_client.get("/api/characters/?show-all=yes")
        count_all = api_client.get("/api/characters/count/?show-all=yes")
        assert list_all.data["count"] == count_all.data["count"]

    @staticmethod
    def test_pagination_structure_consistent(api_client: APIClient, character_with_issues: Character) -> None:
        """Test that pagination structure is consistent."""
        response = api_client.get("/api/characters/")

        assert response.status_code == 200
        assert response.data["count"] is not None
        assert response.data["next"] is None or isinstance(response.data["next"], str)
        assert response.data["previous"] is None or isinstance(response.data["previous"], str)
        assert isinstance(response.data["results"], list)
