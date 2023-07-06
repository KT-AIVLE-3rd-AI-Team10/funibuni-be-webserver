from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from accounts.serializers import UserSerializer,AddressSerializer
from accounts.models import User,Address
from accounts.serializers import PhoneNumberLoginSerializer
from accounts.models import BlacklistedToken,OutstandingToken
from accounts.auth.authentications import JWTAuthenticationForRefresh
from django.db import IntegrityError

# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # 저장할 주소 정보 추출
        phone_number = request.data.get('phone_number')
        name = request.data.get('name')
        disposal_location = request.data.get('disposal_location')
        postal_code = request.data.get('postal_code')
        address_road = request.data.get('address_road')
        address_land = request.data.get('address_land')
        address_district = request.data.get('address_district')
        address_dong = request.data.get('address_dong')
        address_city = request.data.get('address_city')
        address_detail = request.data.get('address_detail')

        # Address 모델에 저장
        address = Address(
            user=user,
            disposal_location=disposal_location,
            postal_code=postal_code,
            address_road=address_road,
            address_land=address_land,
            address_district=address_district,
            address_dong=address_dong,
            address_city=address_city,
            address_detail=address_detail
        )
        address.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        address_serializer = AddressSerializer(address)
        return Response({
            'access_token': str(access),
            'refresh_token': str(refresh),
            'address': address_serializer.data  # 주소 정보를 응답에 포함
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
@permission_classes([IsAuthenticated])
def auto_signin(request):
    refresh_token = request.headers.get('Authorization')

    if refresh_token:
        refresh_token = refresh_token.replace('Bearer ', '')

        try:
            # 블랙리스트 확인
            if BlacklistedToken.objects.filter(token=refresh_token).exists():
                return Response({'error': 'Token is blacklisted'}, status=status.HTTP_400_BAD_REQUEST)

            # 사용자 식별 정보 얻기
            user_id= User.objects.get(id=request.user.id)  # 사용자 객체 가져오기
            user_serializer = UserSerializer(user_id)

            # 새로운 액세스 토큰과 리프레시 토큰 발급
            new_refresh = RefreshToken.for_user(user_id)  # 사용자 식별 정보를 리프레시 토큰에 포함
            new_access_token = str(new_refresh.access_token)
            new_refresh_token = str(new_refresh)

            # 기존 토큰을 블랙리스트에 추가
            BlacklistedToken.objects.create(token=refresh_token)  # 사용자 식별 정보 저장

            return Response({'access_token': new_access_token, 'refresh_token': new_refresh_token}, status=200)
        except TokenError as e:
            return Response({'error': str(e)}, status=401)
    else:
        return Response({'error': 'Refresh token is required'}, status=400)

#access토큰 재발급
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def token_refresh(request):
    refresh_token = request.headers.get('Authorization')

    if refresh_token:
        refresh_token = refresh_token.replace('Bearer ', '')

        try:
            refresh = RefreshToken(refresh_token)
            
            # 블랙리스트 확인
            if BlacklistedToken.objects.filter(token=refresh_token).exists():
                return Response({'error': 'Token is blacklisted'}, status=status.HTTP_400_BAD_REQUEST)
            
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=200)
        except TokenError as e:
            return Response({'error': str(e)}, status=401)
    else:
        return Response({'error': 'Refresh token is required'}, status=400)

#로그아웃 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
        address = Address.objects.filter(user=user).first()

        user_serializer = UserSerializer(user)
        address_serializer = AddressSerializer(address) if address else None

        response_data = {
            'user': user_serializer.data,
            'address': address_serializer.data if address_serializer else None
        }

        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
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
            return Response({'error': 'Token is blacklisted'}, status=status.HTTP_400_BAD_REQUEST)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

#주소 생성 및 조회/삭제
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def address_create_view(request):
    user = request.user

    if request.method == 'GET':
        addresses = Address.objects.filter(user=user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        disposal_location = request.data.get('disposal_location')
        postal_code = request.data.get('postal_code')
        address_road = request.data.get('address_road')
        address_land = request.data.get('address_land')
        address_district = request.data.get('address_district')
        address_dong = request.data.get('address_dong')
        address_city = request.data.get('address_city')

        address = Address(
            user=user,
            disposal_location=disposal_location,
            postal_code=postal_code,
            address_road=address_road,
            address_land=address_land,
            address_district=address_district,
            address_dong=address_dong,
            address_city=address_city
        )
        address.save()

        return Response({'message': 'Address created successfully'}, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        address_id = request.data.get('address_id')  

        try:
            address = Address.objects.get(address_id=address_id, user=user)
            address.delete()
            return Response({'message': 'Address deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response({'message': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)