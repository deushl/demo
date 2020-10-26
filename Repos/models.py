from django.dispatch import receiver
from django.db import models
from Users.models import Users
from datetime import datetime
from django.db.models.signals import post_save

# Create your models here.


class Repo(models.Model):
    uuid = models.IntegerField(unique=True)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='repos')
    name = models.CharField(max_length=256, null=False)
    started_at = models.DateTimeField(null=False, default=datetime.now())
    json_blob = models.TextField()
    open_issues = models.IntegerField(null=False, default=0)
    total_commits = models.IntegerField(null=False, default=0)


class Contributor(models.Model):
    uuid = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=256)
    repo = models.ForeignKey(
        Repo, related_name='contributors', on_delete=models.CASCADE)
    contributions = models.IntegerField()


@receiver(post_save, sender=Contributor)
def on_contributor_save(sender, instance, **kwargs):
    repo_uuid = instance.repo.uuid

    repo = Repo.objects.get(uuid=repo_uuid)
    repo.total_commits = repo.total_commits + instance.contributions
    repo.save()
