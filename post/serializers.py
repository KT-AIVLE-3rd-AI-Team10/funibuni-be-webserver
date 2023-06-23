from rest_framework import serializers
from post.models import Post,PostReport,PostLike,Comment,CommentReport,Reply,ReplyReport
from accounts.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    is_sharing = serializers.IntegerField(default=0)  # 기본값으로 0 설정
    user = serializers.SerializerMethodField()
    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_user(self, obj):
        user_data = {
            'user_id': obj.user.id,
            'nickname': obj.user.nickname
        }
        return user_data
    class Meta:
        model = Post
        fields = ['post_id', 'user', 'title', 'content', 'expired_date', 'image_url',
                  'product_top_category', 'product_mid_category', 'product_low_category',
                  'address_city', 'address_district', 'address_dong', 'created_at', 'is_sharing',
                  'comments_count', 'likes_count']
        
class PostReportSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = PostReport
        fields = ['post_id', 'user_id', 'created_at']

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post_like_id', 'post_id', 'user_id', 'created_at']
        
class CommentReportSerializer(serializers.ModelSerializer):
    comment = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommentReport
        fields = ['comment_report_id', 'comment', 'user', 'created_at']
        
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post_id = serializers.PrimaryKeyRelatedField(source='post', read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'post_id', 'user', 'comment', 'created_at']

    def get_user(self, obj):
        user_data = {
            'user_id': obj.user.id,
            'nickname': obj.user.nickname
        }
        return user_data
    
class ReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    comment_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reply
        fields = ['reply_id', 'user', 'comment_id', 'reply', 'created_at']
    
    def get_user(self, obj):
        user_data = {
            'user_id': obj.user_id,
            'nickname': obj.user.nickname
        }
        return user_data

class ReplyReportSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    reply = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReplyReport
        fields = ['reply_report_id', 'reply', 'user', 'created_at']
        
    def to_representation(self, instance):
        # 대댓글을 신고한 사용자와 현재 인증된 사용자가 동일한 경우, 대댓글을 숨김
        if instance.reports.filter(user=self.context['request'].user).exists():
            return {}  # 대댓글을 숨기기 위해 빈 딕셔너리를 반환합니다.
        return super().to_representation(instance)