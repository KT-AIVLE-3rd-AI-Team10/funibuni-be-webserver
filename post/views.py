from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user
    title = request.data.get('title')
    content = request.data.get('content')

    # 게시물 생성 로직
    post = Post.objects.create(user=user, title=title, content=content)

    # 생성된 게시물 정보 반환
    serializer = PostSerializer(post)
    return Response(serializer.data, status=201)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data, status=200)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=204)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # post와 user 필드는 수정되지 않도록 제외합니다.
        serializer = CommentSerializer(comment, data=request.data, partial={'post', 'user'})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=204)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    user = request.user
    comment_text = request.data.get('comment')

    if not comment_text:
        return Response({'error': 'Comment cannot be empty.'}, status=400)

    # 댓글 생성 로직
    comment = Comment.objects.create(post=post, user=user, comment=comment_text)

    # 생성된 댓글 정보 반환
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=201) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reply_create(request, post_id, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    post = parent_comment.post
    user = request.user
    reply_text = request.data.get('reply')

    if not reply_text:
        return Response({'error': 'Reply cannot be empty.'}, status=400)

    # 대댓글 생성 로직
    reply = Comment.objects.create(post=post, user=user, parent_comment=parent_comment, comment=reply_text)

    # 생성된 대댓글 정보 반환
    serializer = CommentSerializer(reply)
    return Response(serializer.data, status=201)
@api_view(['GET'])
def post_with_comments(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    post_serializer = PostSerializer(post)
    comment_serializer = CommentSerializer(post.comments.all(), many=True)

    data = {
        'post': post_serializer.data,
        'comments': comment_serializer.data
    }

    return Response(data)