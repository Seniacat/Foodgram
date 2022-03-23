from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views

from .models import Subscription, User
from .serializers import SubscriptionSerializer


class SubscriptionsListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return user.following.all()
