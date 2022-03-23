from django.urls import include, path

from .views import SubscriptionsListView


urlpatterns = [
    path('subscriptions/', SubscriptionsListView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]