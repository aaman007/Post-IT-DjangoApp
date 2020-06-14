from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category' , 'date_published', 'username', 'status']

    def get_username(self, post):
        return post.author.username