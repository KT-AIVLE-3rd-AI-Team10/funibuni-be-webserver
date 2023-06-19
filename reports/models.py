from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)