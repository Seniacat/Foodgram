import re
from tkinter.tix import Tree
from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, serializers, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import SubscriptionSerializer, SubscribeSerializer
from recipes.pagination import CustomPagination


class CurrentUserViewSet(UserViewSet):
    pagination_class =CustomPagination
   
    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = self.request.user
        following = user.follower.all()
        serializer = SubscriptionSerializer(following, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
            detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        author =get_object_or_404(User, id=id)
        user = self.request.user
        if request.method == 'DELETE':
            subscription = get_object_or_404(Subscription, user=user, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {'author': author.id, 'user': user.id}
        serializer = SubscribeSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
