from rest_framework import serializers

from recipes.models import Ingredient, IngredientsInRecipe, Recipe
from tags.models import Tag
from users.models import User


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipeSerializer():
    pass