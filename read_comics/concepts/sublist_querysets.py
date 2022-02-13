from read_comics.issues.view_mixins import IssuesSublistQueryset
from read_comics.volumes.view_mixins import VolumesSublistQueryset


class ConceptSublistQueryset(IssuesSublistQueryset, VolumesSublistQueryset):
    pass
