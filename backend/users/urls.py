from django.urls import include, path

from users.views import SubscriptionViewSet, SubscribeView


urlpatterns = [
    path('users/subscriptions/', SubscriptionViewSet.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', SubscribeView.as_view())
]
