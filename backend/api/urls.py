from django.db import router
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path('auth/', include('djoser.urls')),
]
