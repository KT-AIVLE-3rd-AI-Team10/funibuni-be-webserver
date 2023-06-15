from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # 패스워드 필드 추가

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'address', 'phone_number', 'email', 'password']  # 'password' 필드 포함

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user