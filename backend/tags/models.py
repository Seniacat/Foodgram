from tabnanny import verbose
from django.db import models

class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=255,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=8,
        unique=True
    )
    slug = models.SlugField(
        'Cлаг',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self):
        return self.name