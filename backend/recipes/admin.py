from django.contrib import admin
from django.contrib.admin import site, register

from .models import Ingredient, Recipe, IngredientsInRecipe


class IngredientsInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    
"""
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    list_editable = ('name', 'measurement_unit')"""


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsInRecipeInline,)
    list_filter = ('name', 'tags', 'ingredients')

    """def get_tags(self, obj):
        return ",".join([str(item) for item in obj.tags.all()])"""

    """def get_ingredients(self, obj):
        return ",".join([str(item) for item in obj.ingredients.all()])
"""

admin.site.register(Ingredient)
admin.site.register(IngredientsInRecipe)
admin.site.register(Recipe, RecipeAdmin)
