import django_filters
from django_filters import filters

from users.models import User
from .models import Recipe


class TagFilter(django_filters.FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
                                            method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited')

    def get_is_favorited(self, queryset, name, value):
        return queryset.filter(users_favorites__user=self.request.user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        return queryset.filter(shopping_cart__user=self.request.user)
