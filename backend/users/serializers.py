from dataclasses import fields
from pyexpat import model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Subscription, User


class CurrentUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(method_name='check_following')

    class Meta:
        model = User
        fields = ('email',
                'id',
                'username',
                'first_name',
                'last_name',
                'is_subscribed'
        )

    def check_following(self, obj):
        user = self.context.get('request').user
        if len(Subscription.objects.filter(user=user, author=obj)) == 0:
            return False
        return True


class SubscriptionSerializer(serializers.ModelSerializer):
    author = CurrentUserSerializer(read_only=True)

    def validate(self, data):
        return data

    class Meta:
        model = Subscription
        fields = ('author',)



    