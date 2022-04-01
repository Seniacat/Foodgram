import re
from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import generics, status, serializers, views
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import CurrentUserSerializer, SubscriptionSerializer


class CurrentUserViewSet(UserViewSet):

    @action(detail=False)
    def subscriptions(self, request):
        user = self.request.user
        following = user.follower.all()
        serializer = SubscriptionSerializer(following, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, id):
        author =get_object_or_404(User, id=id)
        user = self.request.user
        if user == author:
            raise serializers.ValidationError('Нельзя подписаться на самого себя!')
        with transaction.atomic:
            Subscription.objects.create(
                                        user=self.request.user,
                                        author=author)
            serializer = CurrentUserSerializer(author, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscription(self, request, id):
        author =get_object_or_404(User, id=id)
        user = self.request.user
        subscription = get_object_or_404(Subscription, user=user, author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)