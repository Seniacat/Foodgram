from colorfield.fields import ColorField
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название',
        help_text='Введите название тега'
    )
    color = ColorField(
        max_length=8,
        unique=True,
        verbose_name='Цвет',
        help_text='Выберите цвет тега'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Cлаг',
        help_text='Введите слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
