import requests
from ._default_data import BASE_USERS
from Users.models import Users
from Repos.models import Repo, Contributor
from datetime import datetime
from demo.env import GITHUB_TOKEN

import json
import pytz


headers = {
    'Authorization': 'token ' + GITHUB_TOKEN
}


def get_initial_user_data():
    for user in BASE_USERS:
        print('Fetching: ' + user['url'])
        r = requests.get(user['url'], headers=headers)
        print(r.status_code)

        print('Saving User data')
        Users.objects.update_or_create(uuid=user['udid'], name=user['name'],
                                       url=user['url'], json_blob=r.text, repo_url=r.json()['repos_url'])


def fetch_repo_data():
    users = Users.objects.all()
    for user in users:
        print('Fetching repos from: ' + user.name + '\n')
        r = requests.get(user.repo_url, headers=headers)
        if r.status_code == 200:
            for repo in r.json():
                print('Saving ' + repo['full_name'])
                blob = {
                    "repo_uuid": repo['id'],
                    "name": repo['name'],
                    "full_name": repo['html_url'],
                    "description": repo['description'],
                    "language": repo['language'],
                    "stats_data": {
                        "size": repo['size'],
                        "stargazers_count": repo['stargazers_count'],
                        "watchers_count": repo['watchers_count'],
                        "has_issues": repo['has_issues'],
                        "has_projects": repo['has_projects'],
                        "has_downloads": repo['has_downloads'],
                        "has_wiki": repo['has_wiki'],
                        "has_pages": repo['has_pages'],
                        "forks_count": repo['forks_count'],
                        "open_issues_count": repo['open_issues_count'],
                        "forks": repo['forks'],
                        "open_issues": repo['open_issues'],
                        "watchers": repo['watchers']
                    },
                    "org_uuid": repo['owner']['id'],
                    "owner_uuid": repo['owner']['node_id'],
                    "started_at": repo['created_at'],
                    "last_push_at": repo['pushed_at']
                }
                repo_obj = Repo.objects.update_or_create(
                    uuid=repo['id'],
                    defaults={
                        'user': Users.objects.get(uuid=repo['owner']['id']),
                        'open_issues': repo['open_issues'],
                        'name': repo['name'],
                        'started_at': pytz.utc.localize(datetime.strptime(
                            repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')),
                        'json_blob': json.dumps(blob)
                    }
                )

                request = requests.get(
                    repo['contributors_url'], headers=headers)

                if request.status_code == 200:
                    for contributor in request.json():
                        print('Adding contributor ' +
                              contributor['login'] + ' to repo: ' + repo['name'])
                        Contributor.objects.update_or_create(
                            uuid=contributor['id'],
                            defaults={
                                'name': contributor['login'],
                                'contributions': contributor['contributions'],
                                'repo': repo_obj[0]
                            }
                        )

                print('OK')
