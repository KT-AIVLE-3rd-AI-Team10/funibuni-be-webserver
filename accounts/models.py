from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number field must be set')
        if not name:
            raise ValueError('The name field must be set')

        nickname = self.generate_nickname(name)  

        extra_fields['nickname'] = nickname  
        
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, name, password,**extra_fields)
    def generate_nickname(self, name):
        nickname = name[0] + '버니'
        return nickname
    
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=255, unique=False)
    nickname = models.CharField(max_length=255, unique=False,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def has_perm(self, perm, obj=None):
        return True
 
    def has_module_perms(self, app_label):
        return True

class BlacklistedToken(models.Model):
    token = models.TextField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

class OutstandingToken(models.Model):
    token = models.TextField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def blacklist(self):
        BlacklistedToken.objects.create(token=self.token)

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disposal_location = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=10)
    address_road = models.CharField(max_length=100)
    address_land = models.CharField(max_length=100)
    address_district = models.CharField(max_length=100)
    address_dong = models.CharField(max_length=100)
    address_city = models.CharField(max_length=100)
    address_detail = models.CharField(max_length=100)
