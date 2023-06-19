from rest_framework.response import Response
from post.models import Post
from post.serializers import PostSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
def get_post_list(request):
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
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

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