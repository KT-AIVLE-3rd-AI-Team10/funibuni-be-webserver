from django.db import models
from accounts.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class UrlImages(models.Model):
    #_id = models.ObjectIdField()
    waste_id = models.AutoField(primary_key=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    image_title = models.TextField(null=True, default="testt.jpg")
    image_url = models.TextField(null=False, default="media/testt.jpg") #FilePathField
    #image_context = models.TextField(null=False, default="일방통행")
    apply_binary = models.IntegerField(default=0)
    postal_code = models.CharField(max_length=255, null=True)
    address_full_lend = models.CharField(max_length=255, null=True)
    address_full_street = models.CharField(max_length=255, null=True)
    address_city = models.CharField(max_length=255, null=True)
    address_district = models.CharField(max_length=255, null=True)
    disposal_location = models.CharField(max_length=255, null=True)
    disposal_datetime = models.CharField(max_length=255, null=True)
    memo = models.CharField(max_length=255, null=True)
    
    class Meta:
        db_table = "url_images"