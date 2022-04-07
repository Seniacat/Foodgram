from rest_framework import mixins, viewsets

from .models import Tag
from .serializers import TagSerializer
from recipes.permissions import IsAdminOrReadOnly


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
