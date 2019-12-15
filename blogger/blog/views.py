#django/rest_framework imports.
from django.shortcuts import render
from django.db.models import Max
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.db.models import F

#app level imports.
from .serializer import(
    BlogPostSerializer,
    ListOfBlogsSerializer,
    CommentPostSerializer,
    ListOfCommentsSerializer,
    ListOfBlogsWithDetailsSerializer,
)
from libs.constants import(
    BAD_ACTION,
    BAD_REQUEST,
)
from libs.exceptions import(
    ParseException,
    ResourceNotFoundException,
)
from .models import (
    Blog,
    Comment,
)
from libs.sort_json_data import sort


class BlogViewSet(GenericViewSet):
    """
    """
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put','delete']
    model = Blog

    permission_classes=[IsAuthenticated, ]

    def get_queryset(self, filterdata=None):
        self.queryset = self.model.objects.all()
        if filterdata:
            self.queryset = self.queryset.filter(**filterdata)
        return self.queryset

    def get_object(self, id):
        try:
            return self.model.objects.get(id=id)
        except Exception as key:
            raise Http404('Invalid id')
            # raise ResourceNotFoundException()

    serializers_dict = {
        'post': BlogPostSerializer,
        'mybloglist': ListOfBlogsSerializer,
        'listofblogs': ListOfBlogsSerializer,
        'mostliked': ListOfBlogsSerializer,
        'mostcommented': ListOfBlogsSerializer,
        'mostdisliked': ListOfBlogsSerializer,
        'mostviewd': ListOfBlogsSerializer,
        'blogsdetails': ListOfBlogsWithDetailsSerializer,
        'getblog': ListOfBlogsWithDetailsSerializer,
    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    @action(methods=['post'], detail=False)
    def post(self, request):
        '''
        Post your blog.
        '''
        data = request.data
        data["author"] = request.user.id

        serializer = self.get_serializer(data=data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        user = serializer.save()
        print(user)
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)     
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def mybloglist(self, request):
        '''
        To get the perticular user blogs.
        '''
        try:
            data = self.get_serializer(self.get_queryset(
                filterdata={"author": request.user}), many=True).data

            page = self.paginate_queryset(data)
            if page is not None:
                return self.get_paginated_response(page)

        except Exception as e:
            return Response({'error':str(e)},
             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=False)
    def deleteblog(self, request):
        '''
        delete blog.
        '''
        try:
            data = self.get_queryset(filterdata={"author": request.user,"id": request.data["id"]})
            data.delete()
            return Response(({"detail": "deleted successfully."}),
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def listofblogs(self, request):
        '''
        List of blogs.
        '''
        try:
            data = self.get_serializer(self.get_queryset(filterdata={'status':'P'}), many=True).data
            page = self.paginate_queryset(data)
            if page is not None:
                return self.get_paginated_response(page)

        except Exception as e:
            return Response({'error':str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(
        methods=['post'], detail=False
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
        methods=['post'], detail=False
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

    @action(methods=['get'], detail=False)
    def mostcommented(self, request):
        '''
        It returns most commentd blog.
        '''
        try:
            data = self.get_serializer(self.get_queryset(filterdata={'status':'P'}), many=True).data
            most_commented = sort(data, 'total_comments')[-1]
            return Response(most_commented, status=status.HTTP_200_OK) 

        except Exception as e:
            return Response(({'error':str(e)}), status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def mostliked(self, request):
        '''
        It returns most liked blog.
        '''
        try:  
            data = self.get_serializer(self.get_queryset(filterdata={'status':'P'}), many=True).data
            most_liked = sort(data, 'total_likes')[-1]
            return Response(most_liked, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(({'error':str(e)}), status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def mostdisliked(self, request):
        '''
        It returns most disliked blog.
        '''
        try:
            data = self.get_serializer(self.get_queryset(filterdata={'status':'P'}), many=True).data
            most_disliked = sort(data, 'total_dislikes')[-1]
            return Response(most_disliked, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(({'error':str(e)}), status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def mostviewd(self, request):
        '''
        It returns most viewd blog.
        '''
        try:
            data = self.get_serializer(self.get_queryset(filterdata={'status':'P'}), many=True).data
            most_disliked = sort(data, 'views')[-1]
            return Response(most_disliked, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(({'error':str(e)}), status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False)
    def getblog(self, request):
        '''
        To get the perticular blog.
        '''
        try:
            self.model.objects.filter(id=request.data['id'], status='P').update(views=F('views')+1) # <-- increament views.
            data = self.get_serializer(self.get_queryset(
            filterdata={"id": request.data['id'], 'status':'P'}), many=True).data
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(({'error':str(e)}), status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False)
    def blogsdetails(self, request):
        '''
        get all the blogs with total views  who commented , who liked, and who disliked.
        '''
        try:
            data = self.get_serializer(self.get_queryset(filterdata={'status':'P'}), many=True).data
            page = self.paginate_queryset(data)
            if page is not None:
                return self.get_paginated_response(page)

        except Exception as e:
            return Response({'error':str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlogsCommentViewSet(GenericViewSet):
    """
    """
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put','delete']
    model = Comment

    permission_classes = [IsAuthenticated, ]

    def get_queryset(self, filterdata=None):
        self.queryset = self.model.objects.all()
        if filterdata:
            self.queryset = self.queryset.filter(**filterdata)
        return self.queryset


    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    serializers_dict = {
        'postcomment': CommentPostSerializer,
        'listcomment': ListOfCommentsSerializer,
    }

    @action(methods=['post'], detail=False)
    def postcomment(self, request):
        '''
        Post your Comment to the Blog.
        '''
        data = request.data
        data["blog"] = request.data['id']

        serializer = self.get_serializer(data=data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        user = serializer.save()
        print(user)
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)     
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def listcomment(self, request):
        '''
        To get the list of Comments for a perticular blog.
        '''
        try:
            data = self.get_serializer(self.get_queryset(
                filterdata={"blog": request.data['id']}), many=True).data

            page = self.paginate_queryset(data)
            if page is not None:
                return self.get_paginated_response(page)

        except Exception as e:
            return Response({'error':str(e)},
             status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=False)
    def deletecomment(self, request):
        '''
        delete comment.
        '''
        try:
            data = self.get_queryset(filterdata={"id": request.data["id"]})
            data.delete()
            return Response(({"detail": "deleted successfully."}),
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)