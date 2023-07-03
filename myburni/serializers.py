from django.db import models
from rest_framework import serializers
from post.models import Post
from waste.models import UrlImages
from accounts.serializers import UserSerializer
from post.serializers import PostSerializer
from waste.serializers import WasteDisposalApplySerializer

class burniSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user_data = {
            'user_id': obj.user.id,
            'nickname': obj.user.nickname
        }
        return user_data

    def to_representation(self, instance):
        if isinstance(instance, list):
            instance.sort(key=lambda x: x.created_at, reverse=True)  # 최신 순으로 정렬

        if isinstance(instance, UrlImages):
            return WasteDisposalApplySerializer(instance).data
        elif isinstance(instance, Post):
            return PostSerializer(instance).data
        else:
            return None
        
    