from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'address', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(id=validated_data['id'], password=password, **validated_data)
        return user