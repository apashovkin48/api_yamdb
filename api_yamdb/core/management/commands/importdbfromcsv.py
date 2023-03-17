from django.core.management.base import BaseCommand
from core.utils import (
    import_user_from_csv,
    import_category_from_csv,
    import_genre_from_csv,
    import_title_from_csv,
    import_review_from_csv,
    import_comment_from_csv
)


class Command(BaseCommand):

    def handle(self, *args, **options):

        print('Start loading data from csv file to DB')

        import_user_from_csv()
        import_category_from_csv()
        import_genre_from_csv()
        import_title_from_csv()
        import_review_from_csv()
        import_comment_from_csv()

        print('Data loading success!')
