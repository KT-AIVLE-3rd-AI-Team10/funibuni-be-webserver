from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.models import User
from accounts.serializers import PhoneNumberLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import BlacklistedToken,OutstandingToken
from accounts.auth.authentications import JWTAuthenticationForRefresh
from django.db import IntegrityError

#회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            'access_token': str(access),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#핸드폰 로그인
@api_view(['POST'])
@permission_classes([AllowAny])
def phone_number_login(request):
    serializer = PhoneNumberLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone_number = serializer.validated_data['phone_number']
    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=400)
    except IntegrityError:
            return Response({'error': 'Token already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)

    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    })

#자동 로그인
@api_view(['POST'])
@permission_classes([AllowAny])
def auto_signin(request):
    refresh_token = request.headers.get('Authorization')

    if refresh_token:
        refresh_token = refresh_token.replace('Bearer ', '')
        # RefreshToken을 사용하여 토큰 유효성 검증
        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            BlacklistedToken.objects.create(token=str(refresh_token))
            new_refresh = RefreshToken.for_user(refresh.get_user())
            new_refresh_token = new_refresh.access_token
            return Response({'access_token': str(access_token),
                             'refresh_token': str(new_refresh_token)}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except IntegrityError:
            return Response({'error': 'Token already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error':  'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

    
#access토큰 재발급
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def token_refresh(request):
    refresh_token = request.headers.get('Authorization')

    if refresh_token:
        refresh_token = refresh_token.replace('Bearer ', '')

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=200)
        except TokenError as e:
            return Response({'error': str(e)}, status=401)
        except IntegrityError:
            return Response({'error': 'Token already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Refresh token is required'}, status=400)
    
#로그아웃 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthenticationForRefresh])
def user_logout_view(request):
    refresh_token = request.headers.get('Authorization')

    if refresh_token:
        refresh_token = refresh_token.replace('Bearer ', '')

        # RefreshToken을 사용하여 토큰 유효성 검증
        try:
            refresh = RefreshToken(refresh_token)
            # 토큰 유효성 검증이 성공한 경우에만 계속 진행합니다.

            # BlacklistedToken 모델을 사용하여 refresh_token을 블랙리스트에 추가합니다.
            BlacklistedToken.objects.create(token=str(refresh_token))

            # OutstandingToken 모델에서도 해당 토큰을 제거합니다.
            OutstandingToken.objects.filter(token=refresh_token).delete()

            return Response({'message': '로그아웃되었습니다.'}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except IntegrityError:
            return Response({'error': 'Token already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
#정보 확인 및 업데이트
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
            # Update only the nickname field
            serializer.save(nickname=request.data.get('nickname', user.nickname))
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#정보 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delete_view(request):
    user = request.user
    refresh_token = request.headers.get('Authorization')

    if refresh_token:
        refresh_token = refresh_token.replace('Bearer ', '')
        try:
            refresh = RefreshToken(refresh_token)
            BlacklistedToken.objects.create(token=str(refresh_token))
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except IntegrityError:
            return Response({'error': '토큰이 이미 블랙리스트에 등록되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)