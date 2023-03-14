from django.db import models


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