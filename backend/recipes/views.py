from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, views, viewsets

from .models import Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer


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


class FavoriteAPIView(views.APIView):

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        

