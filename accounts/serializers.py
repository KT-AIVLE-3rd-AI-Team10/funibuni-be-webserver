from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'name','nickname')

    def create(self, validated_data):
        validated_data['nickname'] = self.generate_nickname(validated_data['name'])
        return super().create(validated_data)
    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.nickname = self.generate_nickname(validated_data['name'])
        instance.save()
        return instance
    def generate_nickname(self, name):
        nickname = name[0] + '버니'
        return nickname
class PhoneNumberLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class PhoneNumberTokenObtainPairView(TokenObtainPairView):
    serializer_class = PhoneNumberLoginSerializer

class PhoneNumberTokenRefreshView(TokenRefreshView):
    pass