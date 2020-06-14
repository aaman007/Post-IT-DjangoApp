from django.db import models
from random import shuffle


class PostManager(models.Manager):

    def get_random_unused_posts(self, category, quantity):
        posts = self.get_queryset().filter(category__icontains=category, status=False)
        post_ids = []
        for post in posts:
            post_ids.append(post.id)
        shuffle(post_ids)
        post_ids = post_ids[:quantity]
        posts = self.get_queryset().filter(id__in=post_ids)
        return posts

    def get_random_used_posts(self, category, quantity):
        posts = self.get_queryset().filter(category__icontains=category, status=True)
        post_ids = []
        for post in posts:
            post_ids.append(post.id)
        shuffle(post_ids)
        post_ids = post_ids[:quantity]
        posts = self.get_queryset().filter(id__in=post_ids)
        return posts


