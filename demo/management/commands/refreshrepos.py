from django.core.management.base import BaseCommand, CommandError
from Users.models import Users
from ._get_data import get_initial_user_data, fetch_repo_data


class Command(BaseCommand):
    help = 'Refreshes the db with the repositories data'

    def handle(self, *args, **options):
        get_initial_user_data()
        fetch_repo_data()

        self.stdout.write('Done')
