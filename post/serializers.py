from django.db import models
from rest_framework import serializers
from post.models import Post,PostReport,PostLike,Comment,CommentReport,Reply,ReplyReport
from accounts.serializers import UserSerializer
from django.db.models import Count

# 게시판
class PostSerializer(serializers.ModelSerializer):
    is_sharing = serializers.BooleanField(default=False) 
    user = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
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
                  'address_city', 'address_district', 'address_dong','created_at', 'is_sharing',
                  'comments_count', 'likes_count']


#게시판 신고     
class PostReportSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    post_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PostReport
        fields = ['post_id', 'user_id', 'created_at']
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.context.get('request')
        return context

    def to_representation(self, instance):
        # 게시물을 신고한 사용자와 현재 인증된 사용자가 동일한 경우, 게시물을 숨김
        if instance.post.reports.filter(user=self.context['request'].user).exists():
            return {}  

        return super().to_representation(instance)

#좋아요!
class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post_like_id', 'post_id', 'user_id', 'created_at']

#댓글 신고
class CommentReportSerializer(serializers.ModelSerializer):
    comment = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommentReport
        fields = ['comment_report_id', 'comment', 'user', 'created_at']

    def to_representation(self, instance):
        # 댓글을 신고한 사용자와 현재 인증된 사용자가 동일한 경우, 댓글을 숨김
        if instance.comment.commentreport_set.filter(user=self.context['request'].user).exists():
            return {}  

        return super().to_representation(instance)

#대댓글
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

#댓글   
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post_id = serializers.PrimaryKeyRelatedField(source='post', read_only=True)
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['comment_id', 'post_id', 'user', 'comment', 'created_at', 'reply_count']

    def get_user(self, obj):
        user_data = {
            'user_id': obj.user.id,
            'nickname': obj.user.nickname
        }
        return user_data

    def get_reply_count(self, obj):
        return obj.reply_set.count()

#대댓글 신고
class ReplyReportSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    reply = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReplyReport
        fields = ['reply_report_id', 'reply', 'user', 'created_at']

    def to_representation(self, instance):
        # 대댓글을 신고한 사용자와 현재 인증된 사용자가 동일한 경우, 대댓글을 숨김
        if instance.reply.reports.filter(user=self.context['request'].user).exists():
            return {}  # 대댓글을 숨기기 위해 빈 딕셔너리를 반환합니다.
        return super().to_representation(instance)
    
# 게시판 상세
class PostdetailSerializer(serializers.ModelSerializer):
    is_sharing = serializers.BooleanField(default=False)  # 기본값으로 0 설정
    user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
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
    def get_is_like(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False
    
    class Meta:
        model = Post
        fields = ['post_id', 'user', 'title', 'content', 'expired_date', 'image_url',
                  'product_top_category', 'product_mid_category', 'product_low_category',
                  'address_city', 'address_district', 'address_dong','created_at', 'is_sharing',
                  'comments_count','is_like','likes_count','comments']
    
