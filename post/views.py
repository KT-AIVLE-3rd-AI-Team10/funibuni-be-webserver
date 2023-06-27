from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from post.serializers import PostSerializer,PostReportSerializer,PostLikeSerializer,CommentReportSerializer,CommentSerializer,ReplySerializer,ReplyReportSerializer
from post.models import Post,User,PostLike,Comment,Reply,ReplyReport

#게시판 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user_id=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#게시판 리스트
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list(request):
    district = request.GET.get('address_district')  # 쿼리 매개변수에서 자치구 값을 가져옴

    posts = Post.objects.all()
    if district:
        posts = posts.filter(address__address_district=district)  # 주소의 자치구를 기준으로 게시물 필터링

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
    
#게시판 상세,수정,삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id, user=request.user)
    except Post.DoesNotExist:
        return Response({'error': '게시물을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'post_id': post_id, 'post': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response({'post_id': post_id}, status=status.HTTP_204_NO_CONTENT)

    return Response({'error': '잘못된 요청입니다.'}, status=status.HTTP_400_BAD_REQUEST)

#나눔완료
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_sharing(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        post.is_sharing = 1  # sharing이 되면 1로 변경
        post.save()
        return Response({'post_id': post_id})
    except Post.DoesNotExist:
        return Response({'error': '게시물을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#나눔 게시글 신고
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_postreport(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': '게시물을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PostReportSerializer(data=request.data, context={'request': request})  # context 인자 추가
    if serializer.is_valid():
        serializer.save(user_id=request.user.id, post_id=post_id)  # user_id, post_id 필드에 직접 값을 전달
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#좋아요!
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_like(request, post_id):
    user = request.user

    if request.method == 'POST':
        try:
            post_like = PostLike.objects.get(post_id=post_id, user=user)
            post_like.delete()
            return Response({'detail': 'Post unliked successfully.'})
        except PostLike.DoesNotExist:
            post_like = PostLike.objects.create(post_id=post_id, user=user)
            serializer = PostLikeSerializer(post_like)
            return Response({'post_id':post_id}, status=201)

    elif request.method == 'DELETE':
        try:
            post_like = PostLike.objects.get(post_id=post_id, user=user)
            post_like.delete()
            return Response({'detail': 'Post like removed successfully.'})
        except PostLike.DoesNotExist:
            return Response({'detail': 'Post like does not exist.'}, status=404)
        
#댓글작성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, post_id):
    user = request.user
    comment_text = request.data.get('comment')

    if not comment_text:
        return Response({'detail': 'Comment cannot be empty.'}, status=400)

    try:
        # 게시물이 존재하는지 확인
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=404)

    # 댓글 생성
    comment = Comment.objects.create(post=post, user=user, comment=comment_text)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=201)

#댓글 수정 및 삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, post_id, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id, user=request.user)
    except Comment.DoesNotExist:
        return Response({'detail': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        comment.delete()
        return Response({'comment_id': comment_id})

    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#댓글 신고
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_report(request,post_id, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({'error': '댓글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CommentReportSerializer(data=request.data, context={'request': request})  # context 인자 추가
    if serializer.is_valid():
        serializer.save(user=request.user, comment=comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#대댓글 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_reply(request, post_id, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({'error': '댓글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        replies = Reply.objects.filter(comment=comment)
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, comment=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#대댓글 수정,삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def reply_detail(request, post_id, comment_id, reply_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({'error': '댓글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        reply = Reply.objects.get(pk=reply_id, comment=comment)
    except Reply.DoesNotExist:
        return Response({'error': '대댓글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = ReplySerializer(reply, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        reply.delete()
        return Response({'comment_id': comment_id}, status=status.HTTP_204_NO_CONTENT)

#대댓글 신고
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reply_report(request, post_id, comment_id, reply_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({'error': '댓글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        reply = Reply.objects.get(pk=reply_id, comment=comment)
    except Reply.DoesNotExist:
        return Response({'error': '대댓글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 대댓글을 신고한 사용자와 현재 인증된 사용자가 동일한 경우, 대댓글을 숨김
    if ReplyReport.objects.filter(reply=reply, user=request.user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ReplyReportSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(reply=reply, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

