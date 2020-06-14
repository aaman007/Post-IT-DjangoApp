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

        #posts = self.get_random_unused_posts(category, quantity)
        #extra_posts = self.get_random_used_posts(category, quantity-posts.count())

        posts = Post.objects.get_random_unused_posts(category=category, quantity=quantity)
        extra_posts = Post.objects.get_random_used_posts(category=category, quantity=quantity-posts.count())

        return posts | extra_posts


    def get_random_unused_posts(self, category, quantity):
        posts = Post.objects.filter(category__icontains=category, status=False)
        post_ids = []
        for post in posts:
            post_ids.append(post.id)
        shuffle(post_ids)
        post_ids = post_ids[:quantity]
        posts = Post.objects.filter(id__in=post_ids)
        return posts


    def get_random_used_posts(self, category, quantity):
        posts = Post.objects.filter(category__icontains=category, status=True)
        post_ids = []
        for post in posts:
            post_ids.append(post.id)
        shuffle(post_ids)
        post_ids = post_ids[:quantity]
        posts = Post.objects.filter(id__in=post_ids)
        return posts