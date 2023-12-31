import base64
from rest_framework import serializers
from .models import UrlImages, WasteSpec
from accounts.models import User
from django.core.files import File
from accounts.serializers import UserSerializer

class UrlImagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UrlImages
        fields = '__all__'  

class WasteSpecSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WasteSpec
        fields = '__all__'  

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
    def to_representation(self, instance):
        data = super().to_representation(instance)
        null_data = {key: value for key, value in data.items() if value is not None}
        if null_data.get('apply_binary') == 0:
            return {}
        return null_data


