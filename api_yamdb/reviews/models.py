from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel
from datetime import datetime

User = get_user_model()


class Genre(models.Model):
    """Модель Genre"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Жанр',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.slug


class Category(models.Model):
    """Модель Category"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Категория',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель Title"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения',
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год издания',
        validators=[
            MaxValueValidator(datetime.now().year)
        ]
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр произведения',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name[:15]


class Review(BaseModel):
    """Модель для отзывов к произведениям (Title)"""
    text = models.TextField(
        verbose_name="Текст отзыва",
        help_text='Введите текст отзыва'
    )
    score = models.IntegerField(
        verbose_name="Оценка произведения",
        help_text='Введите оценку произведения',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Автор отзыва, известен при аутентификации пользователя'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение из базы данных'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(BaseModel):
    """Модель для комментариев к отзывам (Review)"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
