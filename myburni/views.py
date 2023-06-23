from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from post.models import Post
from .serializers import SharingDetailsSerializer

# Create your views here.

#나눔내역
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sharing_list(request):
    posts = Post.objects.all()
    serializer = SharingDetailsSerializer(posts, many=True)
    return Response(serializer.data, status=200)