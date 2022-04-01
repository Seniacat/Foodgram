from django.contrib import admin
from django.contrib.admin import site, register

from .models import (Favorite, Ingredient, Recipe,
                    IngredientsInRecipe)


class IngredientsInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    

class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsInRecipeInline,)
    list_filter = ('name', 'tags', 'ingredients')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )

    """readonly_fields = ('is_favorited',)
    
    def is_favorited(self, instance):
        return instance.favorite_recipes.count()"""

admin.site.register(Ingredient)
admin.site.register(IngredientsInRecipe)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
