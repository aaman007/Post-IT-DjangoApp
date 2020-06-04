from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from django_project.blog.api.serializers import PostSerializer
from django_project.blog.models import Post


@api_view(['GET', ])
def api_detail_post_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.PostNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['PUT', ])
def api_update_post_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.PostNotFount:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data = {'success' : 'update successful'}
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
def api_delete_post_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.PostNotFount:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, request.data)
    operation = post.delete()
    data = {}
    if operation:
        data['success'] = 'delete successful'
    else:
        data['failure'] = 'delete failed'
    return Response(data=data)


@api_view(['POST', ])
def api_create_post_view(request):
    user = User.objects.get(pk=1)

    post = Post(author=user)
    serializer = PostSerializer(post, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



