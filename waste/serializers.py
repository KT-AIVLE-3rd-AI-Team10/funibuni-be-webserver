import base64
from rest_framework import serializers
from .models import PreprocessedImages
from django.core.files import File


class PreprocessedImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PreprocessedImages
        fields = ["image_title", "image_context", "image"]

    def get_image(self, obj):
        try:
            f = open(obj.image_path, 'rb')
            data = base64.b64encode(File(f).read())
            f.close()
            return data
        except IOError:
            f = open("bigproject/media/testt.jpg", "rb")
            data = base64.b64encode(File(f).read())
            f.close()
            return data
        
#모든 폐기물 품목 분류표 정보

#폐기물 배출 신청

#폐기물 배출 신청 상세정보
