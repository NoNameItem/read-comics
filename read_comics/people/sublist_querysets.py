from read_comics.issues.view_mixins import IssuesSublistQueryset
from read_comics.volumes.view_mixins import VolumesSublistQueryset


class PersonSublistQuerysets(IssuesSublistQueryset, VolumesSublistQueryset):
    @staticmethod
    def get_characters_queryset(person):
        return person.created_characters.all().order_by("name", "id")
