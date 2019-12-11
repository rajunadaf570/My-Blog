#django/rest_framework imports.
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

# third part imports.
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

#project level imports.
from blog import views as blog_views

# intialize DefaultRouter.
router = SimpleRouter()

# register blog app urls with router.
router.register(r'blog', blog_views.BlogViewSet, base_name='blog')
router.register(r'comment', blog_views.BlogsCommentViewSet, base_name='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((router.urls, 'api'), namespace='v1')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here
]
