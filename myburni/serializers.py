from django.db import models
from rest_framework import serializers
from post.models import Post
from waste.models import UrlImages
from accounts.serializers import UserSerializer
from post.serializers import PostSerializer
from waste.serializers import WasteDisposalApplySerializer

class burniSerializer(serializers.Serializer):
    model_type = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_model_type(self, obj):
        if isinstance(obj, UrlImages):
            return 'UrlImages'
        elif isinstance(obj, Post):
            return 'Post'
        return None

    def get_data(self, obj):
        if isinstance(obj, UrlImages):
            serializer = WasteDisposalApplySerializer(obj)
        elif isinstance(obj, Post):
            serializer = PostSerializer(obj)
        else:
            return None
        return serializer.data