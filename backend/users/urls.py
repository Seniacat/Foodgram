from django.urls import include, path

from .views import SubscriptionsListView, SubscribeAPIView


urlpatterns = [
    path('users/subscriptions/', SubscriptionsListView.as_view()),
    path('users/<int:pk>/subscribe/', SubscribeAPIView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]