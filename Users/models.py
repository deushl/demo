from django.db import models

# Create your models here.


class Users(models.Model):
    uuid = models.IntegerField(null=False, unique=True, primary_key=True)
    name = models.CharField(max_length=256, null=False, unique=True)
    url = models.CharField(max_length=256, null=False)
    repo_url = models.CharField(max_length=256, null=False)
    json_blob = models.TextField()
