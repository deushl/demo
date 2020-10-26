from django.shortcuts import render
from utils.lib import BaseView
from django.http import JsonResponse
from Users.models import Users
from Repos.models import Repo, Contributor
from django.db.models import Sum

# Create your views here.


class Stats(BaseView):

    def get(self, request, *args, **kwargs):

        orgs = Users.objects.all()

        organizations = [
            {
                "Organisation": {
                    "name": x.name
                },
                "most_popular_repo": {
                    "name": x.repos.all().order_by('-total_commits').first().name
                },
                "open_issue_count": x.repos.aggregate(Sum('open_issues'))['open_issues__sum'],
            }
            for x in orgs]

        return JsonResponse({'org_stats': organizations}, status=200)
