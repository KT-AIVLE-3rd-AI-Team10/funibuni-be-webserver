from rest_framework import serializers
from post.models import Post

class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['post_id', 'author_nickname', 'title', 'content', 'created_at']

    def get_author_nickname(self, obj):
        return obj.user.nickname
