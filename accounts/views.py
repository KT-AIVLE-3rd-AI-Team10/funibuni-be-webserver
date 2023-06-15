from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from accounts.models import User
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([AllowAny])
def user_register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            'refresh': str(refresh),
            'access': str(access),
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        'message': 'Logged in successfully.',
        'refresh': str(refresh),
        'access': str(access)
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_logout_view(request):
    logout(request)  # 로그아웃 처리
    return Response({'success': 'Successfully logged out'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update_view(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)  # 부분 업데이트를 허용하기 위해 `partial=True` 설정

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete_view(request):
    user = request.user
    user.delete()
    return Response({'success': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)