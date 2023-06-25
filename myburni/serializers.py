from django.db import models
from rest_framework import serializers
from post.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post_like_id', 'post_id', 'user_id', 'created_at']