from rest_framework.serializers import ModelSerializer
from .models import User,Post,Comment

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
        
        
class PostListSerializer(ModelSerializer):    
    class Meta:
        model = Post
        fields = '__all__'

        
        
class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'

        
