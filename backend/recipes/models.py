from django.db import models
from django.core.validators import MinValueValidator

from tags.models import Tag
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=255,
        db_index=True
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=50
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField('Название', max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    image = models.ImageField(upload_to='media/recipes/', verbose_name='Изображение')
    text = models.TextField('Описание')
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        related_name='recipes',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        null=False,
        validators=(
            MinValueValidator(1, 'Минимальное время: 1 минута',),
        )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    amount = models.PositiveSmallIntegerField('Количество')

    class Meta:
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return self.recipe.name