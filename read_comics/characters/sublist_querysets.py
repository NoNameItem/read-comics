from issues.view_mixins import IssuesSublistQueryset

from read_comics.people.models import Person
from read_comics.volumes.view_mixins import VolumesSublistQueryset


class CharacterSublistQuerysets(IssuesSublistQueryset, VolumesSublistQueryset):
    def get_died_in_queryset(self, character, user=None):
        return self._annotate_issues_as_finished(
            self._break_issues(
                self._annotate_issues(
                    self._order_issues(
                        character.died_in_issues.filter(comicvine_status="MATCHED")
                    ),
                    character
                )
            ),
            user
        )

    @staticmethod
    def get_authors_queryset(character):
        return Person.objects.filter(created_characters=character).filter(
            comicvine_status="MATCHED").distinct().order_by(
            "name")

    @staticmethod
    def get_character_enemies_queryset(character):
        return character.character_enemies.filter(comicvine_status="MATCHED").order_by("name")

    @staticmethod
    def get_character_friends_queryset(character):
        return character.character_friends.filter(comicvine_status="MATCHED").order_by("name")

    @staticmethod
    def get_teams_queryset(character):
        return character.teams.filter(comicvine_status="MATCHED").order_by("name")

    @staticmethod
    def get_team_friends_queryset(character):
        return character.team_friends.filter(comicvine_status="MATCHED").order_by("name")

    @staticmethod
    def get_team_enemies_queryset(character):
        return character.team_enemies.filter(comicvine_status="MATCHED").order_by("name")
