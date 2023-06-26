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

@api_view(['GET'])
def image_modeling(request):
    # 모든 이미지 객체를 가져옵니다.
    images = PreprocessedImages.objects.all()
    # 이미지 객체를 시리얼라이즈합니다.
    serializer = PreprocessedImageSerializer(images, many=True)
    # 시리얼라이즈된 데이터를 응답으로 반환합니다.
    return Response(serializer.data)


# Create your views here.

# views.py

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
#from .. import FileManager as fm

# @csrf_exempt
# @require_POST
# def image_modeling(request):
#     fm.handle_uploaded_file(request.FILES['file'])
#     response = HttpResponse("ok")
#     response.status_code = 200
#     return  response


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


