from read_comics.issues.view_mixins import IssuesSublistQueryset
from read_comics.volumes.view_mixins import VolumesSublistQueryset


class TeamSublistQuerysets(IssuesSublistQueryset, VolumesSublistQueryset):
    def get_disbanded_in_queryset(self, team, user=None):
        return self._annotate_issues_as_finished(
            self._break_issues(
                self._annotate_issues(
                    self._order_issues(team.disbanded_in_issues.filter(comicvine_status="MATCHED")), team
                )
            ),
            user,
        )

    @staticmethod
    def get_characters_queryset(team):
        return team.characters.filter(comicvine_status="MATCHED").order_by("name")

    @staticmethod
    def get_character_enemies_queryset(team):
        return team.character_enemies.filter(comicvine_status="MATCHED").order_by("name")

    @staticmethod
    def get_character_friends_queryset(team):
        return team.character_friends.filter(comicvine_status="MATCHED").order_by("name")
