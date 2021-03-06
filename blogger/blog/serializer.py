#django/rest_framework imports.
from rest_framework import serializers
from django.contrib.auth.models import User


#app level imports.
from .models import (
    Blog,
    Comment,
)


class BlogPostSerializer(serializers.ModelSerializer):
    """
    BlogPost Serializer.
    """
    title = serializers.CharField(required=False, min_length=2)
    content = serializers.CharField(required=False, min_length=2)
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
    List of Blog Serializer.
    """
    total_comments = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'total_likes', 'total_dislikes', 'total_comments','views' )

    def get_total_comments(self, obj):
        return Comment.objects.filter(blog=obj).count()

    def validate(self, data):
        return data


class CommentPostSerializer(serializers.ModelSerializer):
    """
    Post comment serializer.
    """
    comment = serializers.CharField(required=False, min_length=2)
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'blog')

    def create(self, validated_data):
        user = Comment.objects.create(**validated_data)
        user.save()
        return user

class ListOfCommentsSerializer(serializers.ModelSerializer):
    """
    List of comment serializer.
    """
    class Meta:
        model = Comment
        fields = ('id', 'blog_id' , 'comment')


class ListOfBlogsWithDetailsSerializer(serializers.ModelSerializer):
    """
    List of Blog with details serializer.
    """

    comments = serializers.SerializerMethodField()
    who_likes = serializers.SerializerMethodField()
    who_dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'views', 'comments', 'who_likes', 'who_dislikes', )

    def get_comments(self, obj):
        return Comment.objects.filter(blog=obj).values('comment','blog__author__username', )

    def get_who_likes(self, obj):
        return Blog.objects.filter(title=obj).values('likes__username')

    def get_who_dislikes(self, obj):
        return Blog.objects.filter(title=obj).values('dislikes__username')

