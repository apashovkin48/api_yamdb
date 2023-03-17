import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        print('Start loading data from csv file to DB')
        with open('static/data/users.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                User(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                ).save()
                n += 1
                print(f'done {n}')

        print('Loading Category data')
        with open('static/data/category.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                Category(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                ).save()
                n += 1
                print(f'done {n}')

        print('Loading Genre data')
        with open('static/data/genre.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                Genre(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                ).save()
                n += 1
                print(f'done {n}')

        print('Loading Title data')
        with open('static/data/titles.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                category = Category.objects.get(id=row[3])
                Title(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=category
                ).save()
                n += 1
                print(f'done {n}')

        print('Loading Reviews data')
        with open('static/data/review.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            n = 0
            for row in reader:
                title = Title.objects.get(id=row[1])
                author = User.objects.get(id=row[3])
                Review(
                    id=row[0],
                    title_id=title.id,
                    text=row[2],
                    author=author,
                    score=row[4],
                    pub_date=row[5],
                ).save()
                n += 1
                print(f'done {n}')

    print('Loading Comment data')
    with open('static/data/comments.csv', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        n = 0
        for row in reader:
            review_id = Review.objects.get(id=row[1])
            author = User.objects.get(id=row[3])
            Comment.objects.create(
                id=row[0],
                review=review_id,
                text=row[2],
                author=author,
                pub_date=row[4]
            ).save()
            n += 1
            print(f'done {n}')

        print('Data loading success!')
