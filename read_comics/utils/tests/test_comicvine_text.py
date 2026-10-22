import pytest

from read_comics.issues.models import Issue
from read_comics.missing_issues.models import MissingIssue
from read_comics.publishers.models import Publisher
from read_comics.utils.comicvine_text import (
    numerical_issue_number,
    set_lazy_image_sources,
    split_aliases,
    strip_issue_description,
    strip_links,
)
from read_comics.utils.models import ComicvineSyncModel

LINKED = '<p>See <a href="https://cv/x" data-ref-id="1">Batman</a>.</p>'
COVERS = (
    "<p>Story</p><h4>List of covers and their creators:</h4>" '<table data-max-width="true"><tr><td>x</td></tr></table>'
)
LAZY = '<img class="js-lazy-load-image" data-src="https://img/a.jpg" src="data:,"/><img src="https://img/b.jpg"/>'
NUMBERS = [("½", 0.5), ("12", 12.0), ("12.5", 12.5), ("1A", 1.0), ("A", 0), ("", None), (None, None)]


def test_model_strip_links():
    assert ComicvineSyncModel.strip_links(LINKED) == "<p>See Batman.</p>"
    assert ComicvineSyncModel.strip_links("") is None
    assert ComicvineSyncModel.strip_links(None) is None


def test_model_issue_description():
    assert Issue.get_description(COVERS) == "<p>Story</p>"
    assert Issue.get_description(LINKED) == "<p>See Batman.</p>"
    assert Issue.get_description("") == ""
    assert Issue.get_description(None) is None


def test_model_description_property():
    html = Publisher(html_description=LAZY).description
    assert 'src="https://img/a.jpg"' in html
    assert html.count("image-full-size") == 2
    assert Publisher(html_description=None).description == ""


@pytest.mark.parametrize("number, expected", NUMBERS)
def test_model_numerical_number(number, expected):
    for model in (Issue, MissingIssue):
        obj = model(number=number)
        obj.set_numerical_number()
        assert obj.numerical_number == expected


def test_strip_links():
    assert strip_links(LINKED) == "<p>See Batman.</p>"
    assert strip_links("") is None
    assert strip_links(None) is None


def test_strip_issue_description():
    assert strip_issue_description(COVERS) == "<p>Story</p>"
    assert strip_issue_description("") == ""
    assert strip_issue_description(None) is None


def test_set_lazy_image_sources():
    html = set_lazy_image_sources(LAZY)
    assert 'src="https://img/a.jpg"' in html
    assert "image-full-size" not in html
    assert set_lazy_image_sources(LAZY, img_class="image-full-size").count("image-full-size") == 2


@pytest.mark.parametrize("number, expected", NUMBERS)
def test_numerical_issue_number(number, expected):
    assert numerical_issue_number(number) == expected


def test_split_aliases():
    assert split_aliases("Bat-Man\r\nThe Bat\n\n Dark Knight \n") == ["Bat-Man", "The Bat", "Dark Knight"]
    assert split_aliases("") == []
    assert split_aliases(None) == []
