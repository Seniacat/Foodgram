from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from users.models import User

from .models import Favorite, Ingredient, IngredientsInRecipe, Recipe, ShoppingCart
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (IngredientSerializer, AddRecipeSerializer,
                        RecipeSerializer, ShortRecipeSerializer)
from .utils import convert_txt


class IngredientViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-pub_date')
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class =CustomPagination

    def get_serializer_class(self):
        if (self.action == 'list'
        or self.action == 'retrieve'):
            return RecipeSerializer
        else:
            return AddRecipeSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
    
    @action(
            detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request, pk)
        else:
            return self.delete_recipe(Favorite, request, pk)

    @action(
            detail=False,
            permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        CART = {}
        user = request.user       
        cart = IngredientsInRecipe.objects.filter(recipe__shopping_cart__user=user)
        for ingredient in cart:
            name = ingredient.ingredient.name
            amount = ingredient.amount
            measurement_unit = ingredient.ingredient.measurement_unit      
            if (name, measurement_unit) not in CART:
                CART[(name, measurement_unit)] = amount
            else:
                CART[(name, measurement_unit)] += amount
        return convert_txt(CART)

    @action(
            detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
    )
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