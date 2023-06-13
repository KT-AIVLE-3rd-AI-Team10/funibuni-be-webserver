# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
# from django.contrib.auth.models import User
# from accounts.models import User


class District(models.Model):
    district_id = models.IntegerField(primary_key=True)
    district_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'district'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    email = models.CharField(max_length=45)

    class Meta:
        # managed = False
        db_table = 'user'
    def __str__(self):
        return self.name

    

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    title = models.CharField(max_length=45)
    content = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    left_day = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'post'
        
    def __str__(self):
        return self.title

class Comment(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    user_id = models.IntegerField()
    comment = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # managed = False
        db_table = 'comment'

    def __str__(self):
        return f'{self.post} {self.comment}'