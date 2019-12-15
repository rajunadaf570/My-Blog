# python imports
import uuid

#django/rest_framework imports.
from django.db import models
from django.contrib.auth.models import User

# project level imports
from libs.models import TimeStampedModel

# third party imports
from model_utils import Choices


class Blog(TimeStampedModel):
    """
    Blog model represents the blog in the database.
    """
    STATUS = Choices(
        ('D', 'Draft'),
        ('P', 'Publish'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    status = models.CharField(choices=STATUS, max_length=1, default='D')
    views = models.BigIntegerField(default=0)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='blog'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_dislikes(self):
        return self.dislikes.count()


class Comment(TimeStampedModel):
    """
    Comment model represent list of comments in perticular Blog.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='blog'
    )
    class Meta:
        ordering = ['-created_at']
