from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reports.serializers import ReportSerializer
from django.shortcuts import get_object_or_404
from post.models import Post

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    serializer = ReportSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(post=post, reporter=request.user)
        # 게시물을 비활성화하는 로직 추가
        post.is_active = False
        post.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)