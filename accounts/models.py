from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number field must be set')
        if not name:
            raise ValueError('The name field must be set')

        nickname = self.generate_nickname(name)  # 닉네임 생성

        extra_fields['nickname'] = nickname  # extra_fields에 nickname 추가

        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, name, **extra_fields)

    def generate_nickname(self, name):
        # 여기에서 닉네임을 생성하는 로직을 작성합니다.
        # 예시: 성(first name) + '버니'
        first_name = name.split()[0]  # 이름 추출
        nickname = first_name + '버니'
        return nickname
    def update_nickname(self, user, nickname):
        user.nickname = nickname
        user.save()
        return user

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

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['phone_number', 'name']

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
        