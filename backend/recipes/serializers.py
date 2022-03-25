from dataclasses import fields
from rest_framework import serializers

from recipes.models import Ingredient, IngredientsInRecipe, Recipe
from tags.models import Tag
from tags.serializers import TagSerializer
from users.models import User


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    # author = 
    
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'name', 'author', 'image', 'ingredients', 'text')