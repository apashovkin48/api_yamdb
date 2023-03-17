from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Start loading data from csv file to DB')

        # Your code for load, import from core

        print('Data loading success!')
