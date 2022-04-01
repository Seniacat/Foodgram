from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from users.models import User

from .models import Favorite, Ingredient, Recipe
from .serializers import (IngredientSerializer, AddRecipeSerializer,
                        RecipeSerializer, ShortRecipeSerializer)


class IngredientViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if (self.action == 'list'
        or self.action == 'retrieve'):
            return RecipeSerializer
        else:
            return AddRecipeSerializer

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if Favorite.objects.filter(recipe=recipe, user=user).exists():
            raise ValidationError('Рецепт уже добавлен в избранное')
        with transaction.atomic:
            Favorite.objects.create(recipe=recipe, user=user)
            serializer = ShortRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def del_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        favorite = get_object_or_404(Favorite, recipe=recipe, user=user)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

