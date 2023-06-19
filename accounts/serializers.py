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

    def generate_nickname(self, name):
        # 여기에서 닉네임을 생성하는 로직을 작성합니다.
        # 예시: 성(first name) + '버니'
        first_name = name.split()[0]  # 이름 추출
        nickname = first_name + '버니'
        return nickname
    def update(self, instance, validated_data):
        # 닉네임 필드만 부분 업데이트를 허용합니다.
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()
        return instance

class PhoneNumberLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class PhoneNumberTokenObtainPairView(TokenObtainPairView):
    serializer_class = PhoneNumberLoginSerializer

class PhoneNumberTokenRefreshView(TokenRefreshView):
    pass