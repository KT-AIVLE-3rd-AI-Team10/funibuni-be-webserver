from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.paginator import Paginator
from .models import Post,User,Comment
from .serializers import PostSerializer,CommentSerializer,UserSerializer,PostListSerializer

#user 이건 나중에 account 로 따로 앱..
@api_view(['GET','POST'])
def getTestDatas(request):
    if request.method == 'GET':
        datas = User.objects.all()
        serializer = UserSerializer(datas, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
        
# GET : 나눔게시판 첫 화면 에서 모든 게시글들 보여주기 & POST : 게시글 등록  
@api_view(['GET','POST'])
def post_list(request):
    if request.method == 'GET':
        datas = Post.objects.all()
        paginator = Paginator(datas, 2)  # 한 페이지에 2개씩 표시
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = PostListSerializer(page_obj, many=True)
        return Response(serializer.data)
    # elif request.method == 'POST':
    #     serializer = PostListSerializer(data=request.data)
    #     if serializer.is_valid() :
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    
# 게시글 클릭 했을때 세부사항 보여주는데 게시글 수정과 삭제 넣어주기.    
@api_view(['GET','PUT','DELETE'])
def post_detail(request,pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # 해당 되는 게시글 보여주기
        # print(post)
        serializer = PostSerializer(post)
        # comments = Comment.objects.filter(post=post)
        # comments_serializer = CommentSerializer(comments, many=True)
        # serializer.data['comments'] = comments_serializer.data
        return Response(serializer.data)
    # elif request.method == "PUT":
    #     # 해당 되는 게시글 수정
    #     serializer = PostSerializer(post,data=request.data)
    #     if serializer.is_valid() :
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    # elif request.method == 'DELETE':
    #     # 해당 되는 게시글 삭제
    #     post.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET','POST'])
def comment_list(request, pk):
    try:
        # 해당되는 게시글 추출
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # 해당 되는 게시글의 댓글들 추출
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # 해당 되는 게시글에 댓글 생성
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET','DELETE'])
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)