from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

import ultralytics
from ultralytics import YOLO
from django.core.files import File
from rest_framework.response import Response
from .models import UrlImages
from .serializers import ImageSerializer
import boto3
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os 
import shutil


#def waste_apply(request):
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
            
        new_image = UrlImages(image_title=image.name, image_url=s3_url, user = request.user)
        new_image.save()
        
        ######## 모델링
        yolo_model = YOLO('waste/yolo/best_model/best.pt')
        
        #file_name = os.path.join('/', s3_url)
        result = yolo_model.predict(source=s3_url, save=True, save_txt = True, save_conf = True, conf = 0.15) 
        
        ######## 라벨, 확률 추출
        directory_path = "runs/detect/predict/labels/"
        result_dict = {}
        
        for filename in os.listdir(directory_path): 
            if filename.endswith(".txt"):
                with open(os.path.join(directory_path, filename), 'r') as file:
                    lines = file.readlines()  # 파일의 모든 라인을 읽기

                # 각 라인에 대해
                for i, line in enumerate(lines, start=1):
                    numbers = line.split()  # 라인을 공백을 기준으로 분리하여 숫자 리스트 생성
                    label = int(numbers[0])  # 리스트의 첫번째 숫자 추출
                    probability = round(float(numbers[-1]),2)  # 리스트의 마지막 숫자 추출

                    result_dict[i] = (label, probability)  # 인덱스와 (첫번째 숫자, 마지막 숫자) 튜플을 딕셔너리에 추가
    
        default_storage.delete(path)
        shutil.rmtree('C:/Users/User/Desktop/aivle/6m/bigproject/backend/aivle-ai-team10-be-webserver/runs')
        
        return Response({"message": "Image uploaded successfully.",
                         'image_title': str(image),
                         'image_url': str(file_name),
                         'labels' : result_dict,
                         'waste_id': new_image.pk,
                         }, status=200) 
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