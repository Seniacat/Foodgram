from django.db import transaction
from rest_framework import serializers, validators
from drf_extra_fields.fields import Base64ImageField

import users.serializers as users
from recipes.models import (Favorite, Ingredient,
                            IngredientsInRecipe, Recipe, ShoppingCart)
from tags.models import Tag
from tags.serializers import TagField


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
                        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    validators = (
            validators.UniqueTogetherValidator(
                queryset=IngredientsInRecipe.objects.all(),
                fields=('ingredient', 'recipe')
            ),
        )

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = users.CurrentUserSerializer()
    tags = TagField(
        slug_field='id', queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientInRecipeSerializer(
        source='ingredient_in_recipe',
        read_only=True, many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
                'id',
                'tags',
                'name',
                'author',
                'ingredients',
                'image',
                'text',
                'cooking_time',
                'is_favorited',
                'is_in_shopping_cart'
        )

    def in_list(self, obj, model):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return model.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        return self.in_list(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.in_list(obj, ShoppingCart)


class AddRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
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
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.save()
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = ingredient['id']
            IngredientsInRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
        return recipe

    @transaction.atomic
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
            amount = ingredient['amount']
            ingredient = ingredient['id']
            IngredientsInRecipe.objects.create(
                recipe=instance,
                ingredient=ingredient,
                amount=amount
            )
        instance.tags.clear()
        instance.tags.set(tags)
        return self.instance

    def validate_ingredients(self, data):
        if not data:
            raise serializers.ValidationError(
                'Поле с ингредиентами не может быть пустым'
            )
        unique_ings = []
        for ingredient in data:
            name = ingredient['id']
            if ingredient['amount'] == 0:
                raise serializers.ValidationError(
                    f'Введите количество для {name}'
                )
            if name not in unique_ings:
                unique_ings.append(name)
            else:
                raise serializers.ValidationError(
                    'В рецепте не может быть повторяющихся ингедиентов'
            )
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше 1 минуты'
            )
        return data


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
