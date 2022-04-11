from re import A
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.shortcuts import get_list_or_404
from users.models import Subscription, User
from users.serializers import SubscriptionSerializer, SubscribeSerializer
from recipes.pagination import CustomPagination
from recipes.permissions import IsOwnerOrReadOnly


class SubscriptionViewSet(ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        following = user.follower.all()
        return following

class SubscribeView(views.APIView):
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = self.request.user
        data = {'author': author.id, 'user': user.id}
        serializer = SubscribeSerializer(
                                        data=data,
                                        context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = self.request.user
        subscription = get_object_or_404(
                                        Subscription,
                                        user=user,
                                        author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

