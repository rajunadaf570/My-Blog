#django/rest_framework imports.
from django.shortcuts import render
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#app level imports.
from .serializer import(
    BlogPostSerializer,
    ListOfBlogsSerializer,
)
from libs.constants import(
    BAD_ACTION,
    BAD_REQUEST,
)
from libs.exceptions import(
    ParseException,
)
from .models import (
    Blog,
)
class BlogViewSet(GenericViewSet):
    """
    """
    queryset = Blog.objects.all()

    def get_queryset(self,filterdata=None):
        if filterdata:
            self.queryset = Blog.objects.filter(**filterdata)
        return self.queryset

    def get_object(self, id):
        try:
            return Blog.objects.get(id=id)
        except Exception as e:
            raise Http404('Invalid id')


    serializers_dict = {
        'post': BlogPostSerializer,
        'mybloglist': ListOfBlogsSerializer,
        'listofblogs': ListOfBlogsSerializer,
        # 'like': ListOfBlogsSerializer,
    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ])
    def post(self, request):
        '''
        Post a blog.
        '''
        data = request.data
        data["author"] = request.user.id

        serializer = self.get_serializer(data=data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        user = serializer.create(serializer.validated_data)
        print(user)
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)     
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
    def mybloglist(self, request):
        '''
        To get the perticular user blogs.
        '''
        try:
            data = self.get_serializer(self.get_queryset({"author": request.user}), many=True).data
            page = self.paginate_queryset(data)
            if page is not None:
                return self.get_paginated_response(page)

        except Exception as e:
            return Response({'error':str(e)},
             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=False, permission_classes=[IsAuthenticated, ])
    def deleteblog(self, request):
        '''
        delete the blog.
        '''
        try:
            data = self.get_queryset({"author": request.user,"id": request.data["id"]})
            data.delete()
            return Response(({"detail":"record deleted successfully."}),
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
    def listofblogs(self, request):
        '''
        List of blogs.
        '''
        try:
            data = self.get_serializer(self.get_queryset(), many=True).data
            page = self.paginate_queryset(data)
            if page is not None:
                return self.get_paginated_response(page)

        except Exception as e:
            return Response({'error':str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(
        methods=['post'], detail=False,
        permission_classes=[IsAuthenticated, ]
     )
    def like(self, request):
        '''
        This function will like the perticular blog, but before liking 
        it will remove the dislike.
        '''
        try:
          obj = self.get_object(id=request.data['id'])
          obj.dislikes.remove(request.user)             # <-- remove
          obj.likes.add(request.user)
          return Response(({'status':'ok'}), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(({'error':str(e)}), status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['post'], detail=False, 
        permission_classes=[IsAuthenticated, ]
    )
    def dislike(self, request):
        '''
        This function will dislike the blog, but before disliking it will remove the 
        like.
        '''
        try:
          obj = self.get_object(id=request.data['id'])
          obj.likes.remove(request.user)               # <-- remove 
          obj.dislikes.add(request.user)
          return Response(({'status':'ok'}), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(({'error':str(e)}), status=status.HTTP_400_BAD_REQUEST)
        


