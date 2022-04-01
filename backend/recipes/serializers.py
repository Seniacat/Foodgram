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
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
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

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()


class AddRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    ingredients = AddIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
                'tags',
                'name',
                'ingredients',
                'image',
                'text',
                'cooking_time'
            )

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance)
        return serializer.data

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=request.user)
        for tag in tags:
            recipe.tags.add(tag)
            recipe.save()
        for ingredient in ingredients:
            amount =ingredient['amount']
            ingredient = ingredient['id']
            IngredientsInRecipe.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)
        return recipe
 
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientsInRecipe.objects.filter(recipe=instance).delete()
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
                                                'cooking_time',
                                                instance.cooking_time)
        for ingredient in ingredients:
            amount =ingredient['amount']
            ingredient = ingredient['id']
            IngredientsInRecipe.objects.create(recipe=instance, ingredient=ingredient, amount=amount)
        return self.instance
        

class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')






