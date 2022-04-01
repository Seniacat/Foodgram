from asyncore import read
from tkinter.tix import Tree
from urllib import request
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (Favorite, Ingredient,
                            IngredientsInRecipe, Recipe)
from users.serializers import CurrentUserSerializer
from tags.models import Tag
from tags.serializers import TagField
from users.models import User


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.SlugRelatedField(
                                        source='ingredient',
                                        slug_field='name',
                                        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
                                                    source='ingredient',
                                                    slug_field='measurement_unit',
                                                    read_only=True
    )


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
    ingredients = IngredientInRecipeSerializer(source='ingredient_in_recipe', read_only=True, many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = ('id',
                'tags',
                'name',
                'author',
                'ingredients',
                'image',
                'text',
                'cooking_time',
                'is_favorited'
            )

    # def get_ingredients(self, obj):
        


    """def create(self, validated_data):
        request = self.context.get('request')
        print(validated_data)
        print(request)
        ingredients = validated_data.pop('ingredient_in_recipe')
        tags = validated_data.pop('tags')
        print(ingredients)
        for ing in ingredients:
            print(ing)
            ingredient_id = ing['id']
            amount = ing['amount']
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            IngredientsInRecipe.objects.create(
                                                recipe=recipe,
                                                ingredient=ingredient,
                                                amount=amount)
        return recipe"""

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')






