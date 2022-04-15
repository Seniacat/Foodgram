from django.urls import include, path
from recipes.views import IngredientViewSet, RecipeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
