from dataclasses import fields
from pyexpat import model
from urllib import request
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
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=request.user, author=obj).exists()
    


class SubscriptionSerializer(serializers.ModelSerializer):
    author = CurrentUserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ('author',)

