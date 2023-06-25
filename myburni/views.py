from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from post.models import Post, PostLike
from post.serializers import PostSerializer, PostLikeSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_posts(request):
    user = request.user

    liked_posts = PostLike.objects.filter(user=user).values_list('post', flat=True)
    posts = Post.objects.filter(pk__in=liked_posts)
    post_serializer = PostSerializer(posts, many=True)
    return Response(post_serializer.data, status=status.HTTP_200_OK)