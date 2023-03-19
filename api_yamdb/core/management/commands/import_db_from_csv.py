from django.core.management.base import BaseCommand
from core.utils import import_from_csv


class Command(BaseCommand):
    """
    This command import test data in base from csv file
    """
    def handle(self, *args, **options):

        self.stdout.write('Start loading data from csv file to DB')

        import_from_csv(self, 'users')
        import_from_csv(self, 'category')
        import_from_csv(self, 'genre')
        import_from_csv(self, 'titles')
        import_from_csv(self, 'review')
        import_from_csv(self, 'comments')

        self.stdout.write('Data loading success!')
