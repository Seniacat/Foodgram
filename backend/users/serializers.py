from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Subscription, User
from recipes.models import Recipe
from recipes.serializers import ShortRecipeSerializer


class CurrentUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
                'email',
                'id',
                'username',
                'first_name',
                'last_name',
                'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
                                        user=request.user, author=obj
        ).exists()


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('user', 'author')

    def to_representation(self, instance):
        serializer = SubscriptionSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')
        if user == author:
            raise serializers.ValidationError(
                                'Нельзя подписаться на самого себя!'
            )
        if Subscription.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                                'Вы уже подписаны на этого пользователя!'
            )
        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
                'email',
                'id',
                'username',
                'first_name',
                'last_name',
                'is_subscribed',
                'recipes',
                'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscription.objects.filter(
                    author=obj.author, user=request.user
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.GET.get('recipe_limit'):
            recipe_limit = int(request.GET.get('recipe_limit'))
            print(obj.author)
            queryset = Recipe.objects.filter(
                        author=obj.author).order_by('-pub_date')[:recipe_limit]
        else:
            queryset = Recipe.objects.filter(
                author=obj.author).order_by('-pub_date')
        serializer = ShortRecipeSerializer(queryset, read_only=True, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()
