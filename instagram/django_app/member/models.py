from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    # pass
    def create_user(self, username, password=None):
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        # return self.create_user(username, password)
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class MyUser(PermissionsMixin, AbstractBaseUser):
    # pass

    CHOICES_GENDER = (
        ('m', 'Male'),
        ('f', 'Female')
    )

    # 기본 값
    # password
    # last_login
    # is_active
    # USERNAME이라는 field를 만들고 , USERANME_FIELD에 추가한 후, makemigrations 해보기
    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=20, default='', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER, blank=True, null=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = MyUserManager()


    def get_full_name(self):
        return '{} {}'.format(
            self.nickname,
            self.username
        )

    def get_short_name(self):
        return self.nickname