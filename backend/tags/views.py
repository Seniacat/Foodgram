from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
