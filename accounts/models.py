from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, id, password=None, **extra_fields):
        if not id:
            raise ValueError('The ID field must be set')
        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(id, password, **extra_fields)

class User(AbstractBaseUser):
    id = models.CharField(primary_key=True, max_length=255)
    username = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['username', 'nickname', 'address', 'phone_number', 'email']
    
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
        
