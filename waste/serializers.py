import base64
from rest_framework import serializers
from .models import UrlImages, WasteSpec
from accounts.models import User
from django.core.files import File
from accounts.serializers import UserSerializer

class UrlImagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UrlImages
        fields = '__all__'  # 모든 필드를 serialize

class WasteSpecSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WasteSpec
        fields = '__all__'  # 모든 필드를 serialize

class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'name','nickname')
        
class WasteDisposalApplySerializer(serializers.ModelSerializer):
    user = UserSerializer2(read_only=True) 
    waste_spec_id = WasteSpecSerializer(read_only=True)
    class Meta:
        model = UrlImages
        fields = '__all__'
        

#모든 폐기물 품목 분류표 정보

#폐기물 배출 신청

#폐기물 배출 신청 상세정보
