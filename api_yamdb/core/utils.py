import csv
import os
from users.models import User
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)

# Получаем абсолютный путь до директории проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Генерируем абсолютный путь до файла
file_path = os.path.join(BASE_DIR, 'static/data/users.csv')


def import_user_from_csv():
    print('Start import users from csv file')
    with open(file_path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
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
    print('Finish import user from csv file')


def import_category_from_csv():
    print('Start import category from csv file')
    with open(file_path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            Category(
                id=row[0],
                name=row[1],
                slug=row[2],
            ).save()
    print('Finish import category from csv file')


def import_genre_from_csv():
    print('Start import genre from csv file')
    with open(file_path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            Genre(
                id=row[0],
                name=row[1],
                slug=row[2],
            ).save()
    print('Finish import genre from csv file')


def import_title_from_csv():
    print('Start import title from csv file')
    with open(file_path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            category = Category.objects.get(id=row[3])
            Title(
                id=row[0],
                name=row[1],
                year=row[2],
                category=category
            ).save()
    print('Finish import title from csv file')


def import_review_from_csv():
    print('Start import review from csv file')
    with open(file_path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
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
    print('Finish import review from csv file')


def import_comment_from_csv():
    print('Start import comment from csv file')
    with open(file_path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
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
    print('Finish import comment from csv file')
