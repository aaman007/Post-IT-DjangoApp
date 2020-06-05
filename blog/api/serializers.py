from rest_framework import serializers

from blog.models import Post

MIN_TITLE_LENGTH = 5
MIN_CONTENT_LENGTH = 20


class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date_published', 'username']

    def get_username(self, post):
        return post.author.username


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def validate(self, post):
        '''
        Custom Validation for the data
        '''

        try:
            title = post['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError({'response' : 'Enter a title longer that ' + str(MIN_TITLE_LENGTH)})
            content = post['content']
            if len(content) < MIN_CONTENT_LENGTH:
                raise serializers.ValidationError({"response": 'Enter content longer that ' + str(MIN_CONTENT_LENGTH)})
        except KeyError:
            pass
        return post

