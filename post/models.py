from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from accounts.models import User

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField()
    product_top_category = models.CharField(max_length=255)
    product_mid_category = models.CharField(max_length=255)
    product_low_category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    address_city = models.CharField(max_length=255)
    address_district = models.CharField(max_length=255)
    address_dong = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField()
    is_sharing = models.BooleanField(default=False)
    class Meta:
        db_table = 'post'

class PostReport(models.Model):
    report_id = models.AutoField(primary_key=True, default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_report'

class PostLike(models.Model):
    post_like_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_like'
@receiver(post_save, sender=PostLike)
@receiver(post_delete, sender=PostLike)
def update_likes_count(sender, instance, **kwargs):
    post = instance.post
    post.likes_count = PostLike.objects.filter(post=post).count()
    post.save()

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'

@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def update_comments_count(sender, instance, **kwargs):
    post = instance.post
    post.comments_count = Comment.objects.filter(post=post).count()
    post.save()
        
class CommentReport(models.Model):
    comment_report_id = models.AutoField(primary_key=True)
    comment = models.ForeignKey('post.Comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_report' 
        unique_together = ('comment', 'user')
        
class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reply'

class ReplyReport(models.Model):
    reply_report_id = models.AutoField(primary_key=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reply_report'
        
