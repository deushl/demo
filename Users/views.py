from django.shortcuts import render
from utils.lib import BaseView
from Repos.models import Repo, Contributor
from django.http import JsonResponse
from django.db.models import Sum
from utils.responses import NOT_FOUND

import json

# Create your views here.


class OrgDetails(BaseView):

    def get(self, request, org_uuid, *args, **kwargs):
        repos = Repo.objects.filter(user__uuid=org_uuid).order_by('started_at')
        contributers = Contributor.objects.filter(
            repo__in=repos).order_by('-contributions')

        if len(repos) == 0:
            return JsonResponse(NOT_FOUND, status=404)

        data = {
            "first_repo": json.loads(repos.first().json_blob),
            "last_repo": json.loads(repos.last().json_blob),
            "total_commits": repos.aggregate(Sum('total_commits'))['total_commits__sum'],
            "total_repos": len(repos),
            "top_10_contributors": [{
                'user_uuid': x.uuid,
                'name': x.name,
                'contributions': x.contributions
            } for y, x in enumerate(contributers) if y < 10]
        }

        return JsonResponse(data, status=200)
