from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from users.models import User

from .models import Favorite, Ingredient, Recipe, ShoppingCart
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

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request, pk)
        else:
            return self.delete_recipe(Favorite, request, pk)
        
    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request, pk)
        else:
            return self.delete_recipe(ShoppingCart, request, pk)

    def add_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if model.objects.filter(recipe=recipe, user=user).exists():
            raise ValidationError('Рецепт уже добавлен')
        model.objects.create(recipe=recipe, user=user)
        serializer = ShortRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        obj = get_object_or_404(model, recipe=recipe, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 