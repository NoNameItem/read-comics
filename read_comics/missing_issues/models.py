from django.db import models


# Create your models here.
class IgnoredPublisher(models.Model):
    comicvine_id = models.IntegerField(unique=True)
    comicvine_url = models.URLField(max_length=1000, null=True)
    name = models.TextField(null=True)


class IgnoredVolume(models.Model):
    comicvine_id = models.IntegerField(unique=True)
    comicvine_url = models.URLField(max_length=1000, null=True)
    name = models.TextField()
    start_year = models.CharField(max_length=100, null=True)

    publisher_name = models.TextField(null=True)
    publisher_comicvine_id = models.IntegerField(null=True)


class IgnoredIssue(models.Model):
    comicvine_id = models.IntegerField(unique=True)
    comicvine_url = models.URLField(max_length=1000, null=True)
    name = models.TextField(null=True)
    number = models.CharField(max_length=100, null=True)
    cover_date = models.DateField(null=True)

    volume_comicvine_id = models.IntegerField(unique=True)
    volume_comicvine_url = models.URLField(max_length=1000, null=True)
    volume_name = models.TextField()
    volume_start_year = models.CharField(max_length=100, null=True)

    publisher_name = models.TextField(null=True)
    publisher_comicvine_id = models.IntegerField(null=True)


class MissingIssue(models.Model):
    comicvine_id = models.IntegerField(unique=True)
    comicvine_url = models.URLField(max_length=1000, null=True)
    name = models.TextField(null=True)
    number = models.CharField(max_length=100, null=True)
    cover_date = models.DateField(null=True)

    volume_comicvine_id = models.IntegerField(null=True)
    volume_comicvine_url = models.URLField(max_length=1000, null=True)
    volume_name = models.TextField(null=True)
    volume_start_year = models.CharField(max_length=100, null=True)

    publisher_name = models.TextField(null=True)
    publisher_comicvine_id = models.IntegerField(null=True)
    publisher_comicvine_url = models.URLField(max_length=1000, null=True)

    characters = models.ManyToManyField('characters.Character', related_name='missing_issues')
    concepts = models.ManyToManyField('concepts.Concept', related_name='missing_issues')
    locations = models.ManyToManyField('locations.Location', related_name='missing_issues')
    objects_in = models.ManyToManyField('objects.Object', related_name='missing_issues')
    people = models.ManyToManyField('people.Person', related_name='missing_issues')
    story_arcs = models.ManyToManyField('story_arcs.StoryArc', related_name='missing_issues')
    teams = models.ManyToManyField('teams.Team', related_name='missing_issues')
    volume = models.ForeignKey('volumes.Volume', related_name='missing_issues', on_delete=models.CASCADE, null=True)
    publisher = models.ForeignKey('publishers.Publisher', related_name='missing_issues', on_delete=models.CASCADE,
                                  null=True)

    def __str__(self):
        if self.name:
            return f'{self.volume_name} ({self.volume_start_year}) #{self.number} {self.name}'
        else:
            return f'{self.volume_name} ({self.volume_start_year}) #{self.number}'

    @property
    def publisher_space_path(self):
        return f'{self.publisher_name} [{self.publisher_comicvine_id}]'.replace(':', '*_*').replace('/', '*@*')

    @property
    def volume_space_path(self):
        return f'{self.volume_name} [{self.volume_start_year}] ' \
               f'[{self.volume_comicvine_id}]'.replace(':', '*_*').replace('/', '*@*')

    @property
    def issue_space_path(self):
        return f'{self.volume_name} #{self.number} [{self.comicvine_id}]'.replace(':', '*_*').replace('/', '*@*')

    def ignore_publisher(self):
        p, _ = IgnoredPublisher.objects.get_or_create(
            comicvine_id=self.publisher_comicvine_id,
            defaults={
                'comicvine_url': self.publisher_comicvine_url,
                'name': self.publisher_name
            }
        )
        MissingIssue.objects.filter(publisher_comicvine_id=p.comicvine_id).delete()

    def ignore_volume(self):
        v, _ = IgnoredVolume.objects.get_or_create(
            comicvine_id=self.volume_comicvine_id,
            defaults={
                'publisher_name': self.publisher_name,
                'comicvine_id': self.volume_comicvine_id,
                'comicvine_url': self.volume_comicvine_url,
                'name':  self.volume_name,
                'start_year':  self.volume_start_year
            }
        )
        MissingIssue.objects.filter(volume_comicvine_id=v.comicvine_id).delete()

    def ignore(self):
        i, _ = IgnoredIssue.objects.get_or_create(
            comicvine_id=self.comicvine_id,
            defaults={
                'publisher_name': self.publisher_name,
                'volume_comicvine_id': self.volume_comicvine_id,
                'volume_comicvine_url': self.volume_comicvine_url,
                'volume_name': self.volume_name,
                'volume_start_year': self.volume_start_year,
                'comicvine_id': self.comicvine_id,
                'comicvine_url': self.comicvine_url,
                'name': self.name,
                'number': self.number,
                'cover_date': self.cover_date
            }
        )
        self.delete()
