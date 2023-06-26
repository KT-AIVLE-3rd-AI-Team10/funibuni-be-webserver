from django.db import models
from accounts.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class PreprocessedImages(models.Model):
    #_id = models.ObjectIdField()
    image_title = models.TextField(null=True, default="testt.jpg")
    image_path = models.FilePathField(null=False, default="bigproject/media/testt.jpg")
    image_context = models.TextField(null=False, default="일방통행")

    class Meta:
        db_table = "preprocessed_images"