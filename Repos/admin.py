from django.contrib import admin
from .models import Repo, Contributor
# Register your models here.

admin.site.register([Repo, Contributor])
