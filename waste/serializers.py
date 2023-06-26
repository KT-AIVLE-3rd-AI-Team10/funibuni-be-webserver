import base64
from rest_framework import serializers
from .models import UrlImages
from django.core.files import File



class ImageSerializer(serializers.ModelSerializer):
    #user = serializers.SerializerMethodField(read_only=True)
    waste_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UrlImages
        fields = ['waste_id', 'image_title', 'image_url'] #'user', 
    
        
#모든 폐기물 품목 분류표 정보

#폐기물 배출 신청

#폐기물 배출 신청 상세정보
