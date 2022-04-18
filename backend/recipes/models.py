from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from tags.models import Tag
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Название',
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Введите автора'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
        help_text='Загрузите изображение блюда'
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        related_name='recipes',
        verbose_name='Теги',
        help_text='Выберите теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты'
    )
    cooking_time = models.PositiveSmallIntegerField(
        null=False,
        verbose_name='Время приготовления',
        help_text='Введите время приготовления',
        validators=(
            MinValueValidator(
                settings.MIN_COOK_TIME,
                f'Минимальное время: {settings.MIN_COOK_TIME} минута'
            ),
        )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Ингредиенты'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_list',
        verbose_name='Рецепты'
    )
    amount = models.PositiveSmallIntegerField('Количество')

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient'
            ),
        )
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранные рецепты',
        help_text='Избранные рецепты пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='users_favorites',
        verbose_name='Избранные у пользователей',
        help_text='Избранные рецепты у пользователей'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            ),
        )
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} added {self.recipe} to favorite'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Список покупок',
        help_text='Список покупок пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='В списке у пользователей'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe'
            ),
        )
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user} added {self.recipe} in shopping cart'
