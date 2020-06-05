from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from blog.api.serializers import PostSerializer
from blog.models import Post


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_post_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.PostNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated, ))
def api_update_post_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.PostNotFount:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if post.author != user:
        return Response({'response' : 'You dont have permission to edit that'})

    serializer = PostSerializer(post, request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data = {'success' : 'update successful'}
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, ))
def api_delete_post_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.PostNotFount:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if post.author != user:
        return Response({'response' : 'You dont have permission to delete that'})

    serializer = PostSerializer(post, request.data)
    operation = post.delete()
    data = {}
    if operation:
        data['success'] = 'delete successful'
    else:
        data['failure'] = 'delete failed'
    return Response(data=data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def api_create_post_view(request):
    user = request.user
    post = Post(author=user)
    serializer = PostSerializer(post, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiPostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['title', 'content', 'author__username']

