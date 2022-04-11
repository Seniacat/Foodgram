from rest_framework import serializers

from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')


class TagField(serializers.SlugRelatedField):

    def to_representation(self, value):
        serializer = TagSerializer(value)
        return serializer.data
