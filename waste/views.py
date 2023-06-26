from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import PreprocessedImageSerializer
import ultralytics
from ultralytics import YOLO
from django.core.files import File
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PreprocessedImages
from .serializers import PreprocessedImageSerializer
import boto3
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os 

@api_view(['POST'])
def image_modeling(request):
    if 'image' in request.FILES:
        image = request.FILES['image']
        path = default_storage.save(image.name, ContentFile(image.read()))
        file_name = os.path.join('media/', image.name)
        object_name = os.path.join('0609/', image.name)
        # Boto3를 사용하여 S3 클라이언트를 생성합니다.
        # 'aws_access_key_id', 'aws_secret_access_key'는
        # 실제 AWS 접근 키와 비밀 키로 교체해야 합니다.
        # 'region_name'도 실제 S3 버킷이 위치한 지역으로 교체해야 합니다.
        s3_client = boto3.client(
            's3',
            aws_access_key_id='AKIAZ5NSLTMHIKFFE562',
            aws_secret_access_key='YacwyT8ZiOoxuxBQTBVLQOMCFCjn4MNNnFJJqvrJ',
            #region_name='your_region_name'
        )

        # S3에 이미지를 업로드합니다.
        # 'your_bucket_name'은 실제 S3 버킷 이름으로 교체해야 합니다.
        s3_client.upload_file(file_name, 'furni', object_name)
        
        default_storage.delete(path)
        
        return Response({"message": "Image uploaded successfully."}, status=200)
    
    else:
        return Response({"error": "No image found in request."}, status=400)
    
# @api_view(['GET'])
# def image_modeling(request):
#     # 모든 이미지 객체를 가져옵니다.
#     images = PreprocessedImages.objects.all()
#     # 이미지 객체를 시리얼라이즈합니다.
#     serializer = PreprocessedImageSerializer(images, many=True)
#     # 시리얼라이즈된 데이터를 응답으로 반환합니다.
#     return Response(serializer.data)


# Create your views here.

# views.py

# @api_view(['POST'])
# def image_modeling(request):
#     # Save the input image in the database
#     serializer = PreprocessedImageSerializer(data=request.data)
#     if serializer.is_valid():
#         wasteinfo_obj = serializer.save()
#     else:
#         return Response(serializer.errors, status=400)
    
#     # Load YOLO model
#     yolo_model = YOLO('yolo/best_model/best.pt')
    
#     # Process the image with the YOLO model
#     processed_image_path = yolo_model.predict(source=wasteinfo_obj.input_image.path, save=True)

#     # Save the processed image in the database
#     wasteinfo_obj.output_image = processed_image_path
#     wasteinfo_obj.save()

#     # Return the processed image
#     serializer = WasteImageSerializer(wasteinfo_obj)
#     return Response(serializer.data, status=200)


