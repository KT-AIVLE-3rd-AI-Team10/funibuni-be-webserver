from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

import ultralytics
from ultralytics import YOLO
from django.core.files import File
from rest_framework.response import Response
from .models import UrlImages, WasteSpec
import boto3
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os 
import shutil
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UrlImagesSerializer, WasteSpecSerializer, WasteDisposalApplySerializer
from django.utils import timezone
import pandas as pd

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def waste_detail(request, waste_id):
    try:
        waste = UrlImages.objects.get(waste_id=waste_id)
        serializer = WasteDisposalApplySerializer(waste)
        return Response(serializer.data)
    except UrlImages.DoesNotExist:
        return Response({"error": "Detail not found"}, status=404)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def waste_songpa(request):
    #WasteSpec.objects.all().delete()
    df = pd.read_excel('waste/대형폐기물분류표_송파구.xlsx', sheet_name='퍼니버니', engine='openpyxl')
    
    for index, row in df.iterrows():
        waste_spec = WasteSpec(
            waste_spec_id = index,
            index_large_category=row['index_large_category'],
            index_small_category=row['index_small_category'],
            city='서울',
            district='송파구',
            top_category=row['top_category'],
            large_category=row['large_category'],
            small_category=row['small_category'],
            size_range=row['size_range'],
            is_exists_small_cat_model=row['is_exists_small_cat_model'],
            type=row['type'],
            fee=row['fee'],
        )
        waste_spec.save()

    waste_spec_objects = WasteSpec.objects.all()
    serializer = WasteSpecSerializer(waste_spec_objects, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def waste_apply(request):
    waste_id = request.data.get('waste_id')
    waste_spec_id = request.data.get('waste_spec_id')  # Get waste_spec_id from the request
    if waste_id is None or waste_spec_id is None:
        return Response({"error": "No waste_id or waste_spec_id provided."}, status=400)
    try:
        urlimages = UrlImages.objects.get(waste_id=waste_id)
        waste_spec = WasteSpec.objects.get(waste_spec_id=waste_spec_id)  # Get WasteSpec object with the provided id
    except (UrlImages.DoesNotExist, WasteSpec.DoesNotExist):  # Catch the exception if either object does not exist
        return Response(status=status.HTTP_404_NOT_FOUND)

    urlimages.waste_spec_id = waste_spec  # Assign the WasteSpec object, not just the id
    urlimages.apply_binary = 1
    urlimages.postal_code = request.data.get('postal_code')
    urlimages.address_full_lend = request.data.get('address_full_lend')
    urlimages.address_full_street = request.data.get('address_full_street')
    urlimages.address_city = request.data.get('address_city')
    urlimages.address_district = request.data.get('address_district')
    urlimages.disposal_location = request.data.get('disposal_location')
    urlimages.address_dong = request.data.get('address_dong')
    urlimages.address_detail = request.data.get('address_detail') 
    urlimages.disposal_datetime = timezone.now()
    urlimages.memo = request.data.get('memo')
    urlimages.save()
    
    serializer = UrlImagesSerializer(urlimages)
    return Response(serializer.data)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def image_upload(request):
    if 'image' in request.FILES:
        image = request.FILES['image']
        image_name = image.name.replace('jfif', 'png')
        path = default_storage.save(image_name, ContentFile(image.read()))
        file_name = os.path.join('media/', image_name)
        object_name = os.path.join('django/', image_name)
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
        s3_url = f"https://furni.s3.ap-northeast-2.amazonaws.com/{object_name.replace(' ', '+')}"
        
        #user = User.objects.get(id=request.user.id)
        new_image = UrlImages(image_title=image_name, image_url=s3_url, user = request.user)
        new_image.save()
        
        ######## 모델링
        yolo_model = YOLO('waste/yolo/large_best_model/best.pt')
        
        #file_name = os.path.join('/', s3_url)
        result = yolo_model.predict(source=s3_url, save=True, save_txt = True, save_conf = True, conf = 0.1) 
        
        ######## 라벨, 확률 추출
        directory_path = "runs/detect/predict/labels/"
        directory_path2 = "runs/detect/predict2/labels/"
        
        
        def parse_file():
            handled_labels = set()  # 이미 처리된 라벨을 추적하는 집합
            results = []  # 결과를 저장하는 리스트
            for filename in os.listdir(directory_path): 
                if filename.endswith(".txt"):
                    with open(os.path.join(directory_path, filename), 'r') as file:
                        lines = file.readlines()  # 파일의 모든 라인을 읽기
                        for line in lines:
                            numbers = line.split()  # 라인을 공백을 기준으로 분리하여 숫자 리스트 생성
                            label = int(numbers[0])  # 리스트의 첫번째 숫자 추출
                            probability = round(float(numbers[-1]),2)  # 리스트의 마지막 숫자 추출
                            # 라벨이 이미 처리되었다면 건너뛴다.
                            if label in handled_labels:
                                continue
                            # 라벨을 처리된 라벨 집합에 추가한다.
                            handled_labels.add(label)
                            temp_waste_specs = WasteSpec.objects.filter(index_large_category=label) 
                            temp_category_name = temp_waste_specs.values_list('large_category', flat=True).first()
                            result_dict= {
                                "large-category": {
                                    "index_large_category" : label,
                                    "large_category_name" : temp_category_name,
                                    "probability" : probability
                                },
                                "small-category": []
                                }
                            results.append(result_dict)
                            
            first_label = list(handled_labels)[0]
            # 의자 모델링!
            
            if first_label == 0:
                yolo_model = YOLO('waste/yolo/chair_best_model/best.pt')
                result = yolo_model.predict(source=s3_url, save=True, save_txt = True, save_conf = True, conf = 0.15) 
        
                for filename in os.listdir(directory_path2): 
                    if filename.endswith(".txt"):
                        with open(os.path.join(directory_path2, filename), 'r') as file:
                            lines = file.readlines()  # 파일의 모든 라인을 읽기
                            for line in lines:
                                small_numbers = line.split()  # 라인을 공백을 기준으로 분리하여 숫자 리스트 생성
                                small_label = int(small_numbers[0])  # 리스트의 첫번째 숫자 추출
                                small_probability = round(float(small_numbers[-1]),2)  # 리스트의 마지막 숫자 추출
                                temp_waste_specs = WasteSpec.objects.filter(index_small_category=small_label) 
                                temp_category_name = temp_waste_specs.values_list('small_category', flat=True).first()
                            
                                results[0]["small-category"] = {
                                        "index_small_category" : small_label,
                                        "small_category_name" : temp_category_name,
                                        "probability" : small_probability
                                    }
                                continue
                                                
            # 자전거 모델링!
            if first_label == 2: 
                yolo_model = YOLO('waste/yolo/bicycle_best_model/best.pt')
                result = yolo_model.predict(source=s3_url, save=True, save_txt = True, save_conf = True, conf = 0.15) 
        
                for filename in os.listdir(directory_path2): 
                    if filename.endswith(".txt"):
                        with open(os.path.join(directory_path2, filename), 'r') as file:
                            lines = file.readlines()  # 파일의 모든 라인을 읽기
                            for line in lines:
                                small_numbers = line.split()  # 라인을 공백을 기준으로 분리하여 숫자 리스트 생성
                                small_label = int(small_numbers[0])  # 리스트의 첫번째 숫자 추출
                                small_probability = round(float(small_numbers[-1]),2)  # 리스트의 마지막 숫자 추출
                                temp_waste_specs = WasteSpec.objects.filter(index_small_category=small_label) 
                                temp_category_name = temp_waste_specs.values_list('small_category', flat=True).first()
                            
                                results[0]["small-category"] = {
                                        "index_small_category" : small_label,
                                        "small_category_name" : temp_category_name,
                                        "probability" : small_probability
                                    }
                                continue
                                
            
            return first_label, results
            
        label, results = parse_file()
        
        ## 서버에 남은 불필요한 파일 삭제
        cwd = os.getcwd()
        #parent_dir = os.path.dirname(cwd)
        path_to_remove = os.path.join(cwd, 'runs')
        shutil.rmtree(path_to_remove)
        default_storage.delete(path) 
        image_to_remove = os.path.join(cwd, image_name)
        os.remove(image_to_remove)
        
        #폐기물 분류 표 반환
        large_waste_specs = WasteSpec.objects.filter(index_large_category=label) 
        large_serializer = WasteSpecSerializer(large_waste_specs, many=True)
        large_category_name = large_waste_specs.values_list('large_category', flat=True).first()
        
        all_waste_specs = WasteSpec.objects.all()
        all_serializer = WasteSpecSerializer(all_waste_specs, many=True)
        
        
        return Response({'image_title': str(image),
                         'image_url': str(s3_url),
                         'first_large_category_name' : large_category_name,
                         'labels' : results,
                         'waste_id': new_image.pk,
                         'user' : request.user.id,
                         'first_large_category_waste_specs' : large_serializer.data,
                         'all_waste_specs' : all_serializer.data
                         }, status=200) 
    else:
        return Response({"error": "No image found in request."}, status=400)