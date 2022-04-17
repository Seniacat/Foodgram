from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientsInRecipe, Recipe,
                            ShoppingCart)


class IngredientsInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    search_fields = ('recipe__name', 'ingredient__name')


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_filter = ('name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsInRecipeInline,)
    list_filter = ('tags',)
    search_fields = (
        'name',
        'author__username',
        'author__email'
    )
    readonly_fields = ('is_favorited',)

    def is_favorited(self, instance):
        return instance.favorite_recipes.count()


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe'
    )


admin.site.register(Ingredient)
admin.site.register(IngredientsInRecipe)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
