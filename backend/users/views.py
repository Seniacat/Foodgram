import re
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import CurrentUserSerializer, SubscriptionSerializer


class SubscriptionsListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()


class SubscribeAPIView(views.APIView):

    def post(self, request, pk):
        author =get_object_or_404(User, pk=pk)
        Subscription.objects.create(
                                    user=self.request.user,
                                    author=author)
        serializer = CurrentUserSerializer(author)  # subscribe = False
        return Response(data=serializer.data, status=status.HTTP_200_OK)
