from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Subscription, User


class CustomUserSerializer(UserSerializer):
    pass


class SubscriptionSerializer(serializers.ModelSerializer):
    pass
    