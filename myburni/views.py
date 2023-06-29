from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from post.models import Post, PostLike,Comment
from waste.models import UrlImages
from post.serializers import PostSerializer, PostLikeSerializer,CommentSerializer
from waste.serializers import WasteDisposalApplySerializer
from myburni.serializers import burniSerializer
#나눔 내역 리스트
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def post_list(request):
#     user = request.user
#     posts = Post.objects.exclude(reports__user=user)
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)
#나의 버니 탭
@api_view(['GET'])
def burni_list(request):
    waste_list = UrlImages.objects.order_by('-created_at')[:3]  # 최근에 생성된 3개의 폐기물 데이터 가져오기
    post_list = Post.objects.order_by('-created_at')[:3]  # 최근에 생성된 3개의 게시물 데이터 가져오기
    
    burni_data = list(waste_list) + list(post_list)
    burni_data.sort(key=lambda x: x.created_at, reverse=True)  # 최신 순으로 정렬
    
    result_data = burni_data[:3]  # 가장 최신 3개 데이터 선택
    
    serializer = burniSerializer(result_data, many=True)
    return Response(serializer.data)

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
def post_list(request):
    user = request.user
    posts = Post.objects.filter(user=user)
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

#활동 내역 리스트
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request):
    user = request.user

    # 로그인한 사용자가 작성한 댓글 목록을 조회합니다.
    comments = Comment.objects.filter(user=user)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=200)

