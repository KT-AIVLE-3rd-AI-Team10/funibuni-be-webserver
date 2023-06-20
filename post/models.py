from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, null=False, blank=False)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return self.comment

    