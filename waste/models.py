from django.db import models
from accounts.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class UrlImages(models.Model):
    #_id = models.ObjectIdField()
    image_title = models.TextField(null=True, default="testt.jpg")
    image_url = models.FilePathField(null=False, default="media/testt.jpg")
    #image_context = models.TextField(null=False, default="일방통행")

    class Meta:
        db_table = "url_images"