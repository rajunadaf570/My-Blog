#django/rest_framework imports.
from django.contrib import admin

#project level imports.
from .models import Blog, Comment

# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)