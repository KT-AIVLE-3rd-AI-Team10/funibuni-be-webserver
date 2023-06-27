from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from post.models import Post, PostLike,Comment
from post.serializers import PostSerializer, PostLikeSerializer,CommentSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_posts(request):
    user = request.user

    liked_posts = PostLike.objects.filter(user=user).values_list('post', flat=True)
    posts = Post.objects.filter(pk__in=liked_posts)
    post_serializer = PostSerializer(posts, many=True)
    return Response(post_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request):
    user = request.user

    # 로그인한 사용자가 작성한 댓글 목록을 조회합니다.
    comments = Comment.objects.filter(user=user)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list(request):
    user = request.user
    posts = Post.objects.exclude(reports__user=user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)