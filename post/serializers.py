from rest_framework import serializers
from post.models import Post
from post.models import Comment
class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['post_id', 'author_nickname', 'title', 'content', 'created_at']

    def get_author_nickname(self, obj):
        return obj.user.nickname

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['comment_id', 'post', 'user', 'created_at', 'comment', 'replies']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        serializer = CommentSerializer(replies, many=True)
        serialized_data = serializer.data

        # comment_id를 reply_id로 변경

        return serialized_data