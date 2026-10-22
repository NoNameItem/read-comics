from urllib.parse import parse_qs, urlparse

from read_comics.spiders.spiders.issues_spider import IssuesSpider


def test_list_request_fields():
    fields = parse_qs(urlparse(IssuesSpider.LIST_URL_PATTERN).query)["field_list"][0].split(",")
    assert "associated_images" in fields and "store_date" in fields
