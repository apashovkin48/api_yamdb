from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel


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
    description = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Описание произведения',
    )

    def __str__(self):
        return self.name[15]


class Review(BaseModel):

    text = models.TextField(
        verbose_name="Текст отзыва",
        help_text='Введите текст отзыва'
    )
    score = models.IntegerField(
        verbose_name="Оценка произведения",
        help_text='Введите оценку произведения',
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    # uncommetn after add foreign key model
    """
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
    """

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(BaseModel):
    # after add user logic
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    """
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
