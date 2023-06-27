import base64
from rest_framework import serializers
from .models import UrlImages
from django.core.files import File


class UrlImagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UrlImages
        fields = '__all__'  # 모든 필드를 serialize
        
#모든 폐기물 품목 분류표 정보

#폐기물 배출 신청

#폐기물 배출 신청 상세정보
