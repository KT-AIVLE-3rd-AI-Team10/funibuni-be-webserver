from rest_framework import serializers
from post.models import Post

#최근목록
#class RecentListSerializer(serializers.ModelSerializer):

#나눔내역

class SharingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['post_id', 'title', 'created_at'] ## (city, district), image_url, coment_count


#관심목록

#활동내역

#내정보수정


#배출내역