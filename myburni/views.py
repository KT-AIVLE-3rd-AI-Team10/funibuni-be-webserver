from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from post.models import Post, PostLike,Comment
from waste.models import UrlImages
from post.serializers import PostSerializer, PostLikeSerializer,CommentSerializer
from waste.serializers import WasteDisposalApplySerializer
from myburni.serializers import burniSerializer
from itertools import chain
#나의 버니 탭
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def burni_list(request):
#     waste_list = UrlImages.objects.order_by('-created_at')[:3]  # 최근에 생성된 3개의 폐기물 데이터 가져오기
#     post_list = Post.objects.order_by('-created_at')[:3]  # 최근에 생성된 3개의 게시물 데이터 가져오기
    
#     burni_data = list(waste_list) + list(post_list)
#     burni_data.sort(key=lambda x: x.created_at, reverse=True)  # 최신 순으로 정렬
    
#     serializer = burniSerializer(burni_data, many=True)
    
#     return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def burni_list(request):
    waste_list = UrlImages.objects.filter(user=request.user, apply_binary=1).order_by('-created_at')[:3]  # 현재 사용자가 생성한 폐기물 데이터 가져오기
    post_list = Post.objects.filter(user=request.user, created_at__isnull=False).order_by('-created_at')[:3]  # 현재 사용자가 생성한 게시물 데이터 가져오기
    
    burni_data = list(waste_list) + list(post_list)
    burni_data.sort(key=lambda x: x.created_at, reverse=True)  # 최신 순으로 정렬
    
    waste_serializer = WasteDisposalApplySerializer(waste_list, many=True)
    post_serializer = PostSerializer(post_list, many=True)
    
    data = {
        "user": {
            "user_id": request.user.id,
            "nickname": request.user.nickname
        },
        "posts": post_serializer.data,  # 게시물 데이터 직렬화
        "waste_applies": waste_serializer.data  # 폐기물 데이터 직렬화
    }
    
    return Response(data)

#배출 내역 리스트
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def waste_list(request):
    user = request.user
    urlimages = UrlImages.objects.filter(user=user)  # 현재 사용자가 신청한 폐기물 이미지만 필터링
    
    serializer = WasteDisposalApplySerializer(urlimages, many=True)
    return Response(serializer.data)

#나눔 내역 리스트
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_post(request):
    district = request.GET.get('address_district')
    user = request.user
    posts = Post.objects.filter(user=user)

    if district:
        posts = posts.filter(address_district=district, is_sharing=False)

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
#관심 목록 리스트
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_posts(request):
    user = request.user

    liked_posts = PostLike.objects.filter(user=user).values_list('post', flat=True)
    posts = Post.objects.filter(pk__in=liked_posts)
    post_serializer = PostSerializer(posts, many=True)
    return Response(post_serializer.data, status=status.HTTP_200_OK)

#활동 내역 리스트 // 게시글 목록
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request):
    user = request.user

    # 로그인한 사용자가 작성한 게시물 목록을 조회합니다.
    comments = Comment.objects.filter(user=user)
    posts = [comment.post for comment in comments]  # 해당 댓글이 달린 게시물들을 가져옵니다.
    serializer = PostSerializer(posts, many=True)  # 게시물 시리얼라이저를 사용하여 직렬화합니다.
    return Response(serializer.data, status=200)

