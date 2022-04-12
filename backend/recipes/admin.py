from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe,
                            IngredientsInRecipe, ShoppingCart)


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
    search_fields = (
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
                    'user__email'
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )


admin.site.register(Ingredient)
admin.site.register(IngredientsInRecipe)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
