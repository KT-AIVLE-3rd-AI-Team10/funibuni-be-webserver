from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

import ultralytics
from ultralytics import YOLO
from django.core.files import File
from rest_framework.response import Response
from .models import UrlImages

import boto3
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os 

@api_view(['POST'])
def image_upload(request):
    if 'image' in request.FILES:
        image = request.FILES['image']
        path = default_storage.save(image.name, ContentFile(image.read()))
        file_name = os.path.join('media/', image.name)
        object_name = os.path.join('django/', image.name)
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
        
        s3_url = f"https://furni.s3.ap-northeast-2.amazonaws.com/{object_name}"
        new_image = UrlImages(image_title=image.name, image_url=s3_url)
        new_image.save()
        
        yolo_model = YOLO('waste/yolo/best_model/best.pt')
        
        #file_name = os.path.join('/', s3_url)
        result = yolo_model.predict(source=s3_url, save=True, save_txt = True, save_conf = True, conf = 0.15) 
        
        default_storage.delete(path)
        
        return Response({"message": "Image uploaded successfully.",
                         'image_title': str(image),
                         'image_url': str(file_name),}, status=200)
    else:
        return Response({"error": "No image found in request."}, status=400)
    
'''@api_view(['GET'])
def image_modeling(request):
    # 모든 이미지 객체를 가져옵니다.
    images = PreprocessedImages.objects.all()
    #이미지 객체를 시리얼라이즈합니다.
    serializer = PreprocessedImageSerializer(images, many=True)
    #시리얼라이즈된 데이터를 응답으로 반환합니다.
    return Response(serializer.data)'''