# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import get_user_model
# from phonenumber_field.phonenumber import PhoneNumber

# class PhoneNumberBackend(BaseBackend):
#     def authenticate(self, request, phone_number=None, **kwargs):
#         User = get_user_model()
        
#         try:
#             # 휴대폰 번호로 사용자 검색
#             user = User.objects.get(phone_number=PhoneNumber.from_string(phone_number))
#             return user
#         except User.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         User = get_user_model()
        
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None

