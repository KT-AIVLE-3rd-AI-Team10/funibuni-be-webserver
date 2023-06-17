from django.db import models
from django.contrib.auth import get_user_model

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    nickname = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts', to_field='nickname')
    title = models.CharField(max_length=45)
    content = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    left_day = models.IntegerField()

    class Meta:
        db_table = 'post'
     
    def __str__(self):
        return self.title