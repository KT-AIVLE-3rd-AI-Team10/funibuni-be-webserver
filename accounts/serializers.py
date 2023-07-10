from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.models import User,Address

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = User
        fields = ('user_id', 'phone_number', 'name', 'nickname')

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

class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        address = Address.objects.create(user=user, **validated_data)
        return address