from django.shortcuts import render
from utils.lib import BaseView
from django.http import JsonResponse
from Repos.models import Repo
from django.db.models import Q
from utils.responses import NOT_FOUND

import json


class RepoInfo(BaseView):

    get_params = [
        'owner_uuid',
        'name',
        'started_at'
    ]

    def get(self, request, get_data, *args, **kwargs):

        query = Q()
        repos = Repo.objects.all()

        if get_data['owner_uuid'] is not None:
            query.add(
                Q(user__uuid=int(get_data['owner_uuid'])), Q.AND)
        if get_data['name'] is not None:
            query.add(
                Q(name__contains=get_data['name']), Q.AND)
        if get_data['started_at'] is not None:
            query.add(
                Q(started_at__lte=get_data['started_at']), Q.AND)

        repos = repos.filter(query)

        all_repos = []

        for repo in repos:
            all_repos.append(json.loads(repo.json_blob))

        return JsonResponse(all_repos, status=200, safe=False)


class SingleRepoInfo(BaseView):

    def get(self, request, repo_uuid, * args, **kwargs):

        try:
            repo = Repo.objects.get(uuid=repo_uuid)
        except Repo.DoesNotExist:
            return JsonResponse(NOT_FOUND, status=404)

        return JsonResponse(json.loads(repo.json_blob), status=200)
