#django/rest_framework imports.
from rest_framework import serializers
from django.contrib.auth.models import User


#app level imports.
from .models import (
    Blog,
)


class BlogPostSerializer(serializers.ModelSerializer):
    """
    """
    title = serializers.CharField(required=False, min_length=2)
    content = serializers.CharField(required=False, min_length=2)
    # likes = TagSerializer(read_only=True, many=True)
    # dislikes = TagSerializer(read_only=True, many=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.ChoiceField(
        choices = (
            ('D', 'Draft'),
            ('P', 'Publish'),
        )
    )   
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'author', 'status', )

    def create(self, validated_data):
        user = Blog.objects.create(**validated_data)
        user.save()
        return user

class ListOfBlogsSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'total_likes', 'total_dislikes')


    def validate(self, data):
        return data

