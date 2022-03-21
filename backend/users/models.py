from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        'email',
        unique=True,
        max_length=254
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural ='Пользователи'

    def __str__(self):
        return self.username