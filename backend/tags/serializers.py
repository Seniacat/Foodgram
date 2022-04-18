from rest_framework import serializers

from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')


class TagField(serializers.SlugRelatedField):

    def to_representation(self, value):
        request = self.context.get('request')
        context = {'request': request}
        serializer = TagSerializer(value, context=context)
        return serializer.data
