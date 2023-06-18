from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User, BlacklistedToken
from django.contrib.auth import authenticate, login, logout
#회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def user_register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            'message': '회원가입이 되었습니다.',
            'refresh': str(refresh),
            'access': str(access),
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#로그인
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login_view(request):
    id = request.data.get('id')
    password = request.data.get('password')

    if id is None or password is None:
        return Response({'error': 'ID and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, id=id, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    login(request, user)
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return Response({
        'message': '로그인에 성공하였습니다.',
        'refresh': str(refresh),
        'access': str(access)
    }, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def user_logout_view(request):
#     refresh_token = request.data.get('refresh_token')

#     if refresh_token:
#         # BlacklistedToken 모델을 사용하여 refresh_token을 블랙리스트에 추가합니다.
#         BlacklistedToken.objects.create(token=refresh_token)
#         return Response({'success': 'Successfully logged out'}, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

#로그아웃
@api_view(['POST'])
@permission_classes([AllowAny])
def user_logout_view(request):
    refresh_token = request.headers.get('Authorization')

    if refresh_token:
        refresh_token = refresh_token.replace('Bearer ', '')

        # BlacklistedToken 모델을 사용하여 refresh_token을 블랙리스트에 추가합니다.
        BlacklistedToken.objects.create(token=refresh_token)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({'code': 'Failure'}, status=status.HTTP_400_BAD_REQUEST)
    
# #정보 조회
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_info_view(request):
#     user = request.user
#     serializer = UserSerializer(user)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# # 정보 수정
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def user_update_view(request):
#     user = request.user
#     serializer = UserSerializer(user, data=request.data, partial=True)  # 부분 업데이트를 허용하기 위해 `partial=True` 설정

#     if serializer.is_valid():
#         serializer.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#정보수정 및 업데이트
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_info_view(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#정보 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete_view(request):
    user = request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

