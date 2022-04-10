from django.db import router
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionViewSet, SubscribeView


urlpatterns = [
    path('users/subscriptions/', SubscriptionViewSet.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view())
]
