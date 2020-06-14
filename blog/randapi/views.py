from rest_framework.generics import ListAPIView
from blog.randapi.serializers import PostSerializer
from blog.models import Post
from random import shuffle


class NCategoryListAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = []

    def get_queryset(self):
        #print(request.query_params)
        category = self.kwargs.get('category')
        quantity = self.kwargs.get('quantity')

        posts = Post.objects.get_random_unused_posts(category=category, quantity=quantity)
        extra_posts = Post.objects.get_random_used_posts(category=category, quantity=quantity-posts.count())

        return posts | extra_posts
