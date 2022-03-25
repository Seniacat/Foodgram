from dataclasses import fields
from rest_framework import serializers

from recipes.models import Ingredient, IngredientsInRecipe, Recipe
from users.serializers import CurrentUserSerializer
from tags.models import Tag
from tags.serializers import TagField
from users.models import User


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'

class RecipeSerializer(serializers.ModelSerializer):
    author = CurrentUserSerializer(read_only=True)
    tags = TagField(
        slug_field='id', queryset=Tag.objects.all(), many=True
    )
    
    class Meta:
        model = Recipe
        fields = ('id',
                'tags',
                'name',
                'author',
                'text',
                'cooking_time'
            )