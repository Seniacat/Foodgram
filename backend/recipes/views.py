from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from users.models import User

from .models import Favorite, Ingredient, Recipe
from .serializers import (IngredientSerializer, RecipeSerializer,
                        ShortRecipeSerializer)


class IngredientViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if Favorite.objects.filter(recipe=recipe, user=user).exists():
            raise ValidationError('Рецепт уже добавлен в избранное')
        Favorite.objects.create(recipe=recipe, user=user)
        print(recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        

