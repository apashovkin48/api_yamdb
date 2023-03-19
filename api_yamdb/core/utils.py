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
from api_yamdb.settings import BASE_DIR

# Получаем абсолютный путь до директории проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Генерируем абсолютный путь до файла
file_path = os.path.join(BASE_DIR, 'static/data/users.csv')


def add_user(reader):
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


def add_category(reader):
    for row in reader:
        Category(
            id=row[0],
            name=row[1],
            slug=row[2],
        ).save()


def add_genre(reader):
    for row in reader:
        Genre(
            id=row[0],
            name=row[1],
            slug=row[2],
        ).save()


def add_title(reader):
    for row in reader:
        category = Category.objects.get(id=row[3])
        Title(
            id=row[0],
            name=row[1],
            year=row[2],
            category=category
        ).save()


def add_review(reader):
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


def add_comment(reader):
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


FUNC = {
    'users': add_user,
    'category': add_category,
    'genre': add_genre,
    'titles': add_title,
    'review': add_review,
    'comments': add_comment
}


def import_from_csv(manage_command, file_name: str):
    manage_command.stdout.write(f'Start import {file_name} csv file')
    with (
        open(BASE_DIR / f'static/data/{file_name}.csv', encoding='utf-8')
        as csv_file
    ):
        reader = csv.reader(csv_file)
        next(reader)
        add_func = FUNC.get(file_name)
        add_func(reader)
    manage_command.stdout.write(f'Finish import {file_name} csv file')
