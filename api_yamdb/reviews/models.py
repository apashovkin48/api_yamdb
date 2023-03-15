from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import AbstractUser
from core.models import BaseModel


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
