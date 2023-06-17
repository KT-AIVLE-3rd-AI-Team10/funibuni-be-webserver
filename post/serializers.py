from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    nickname = serializers.CharField(source='nickname.nickname', read_only=True)

    class Meta:
        model = Post
        fields = ['post_id', 'nickname', 'title', 'content', 'created_at', 'left_day']