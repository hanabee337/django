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
    nickname = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)

    # 팔로우 목록을 나타내는 필드 구현
    # 언제 팔로우를 했는지도 나타내도록 함(중간자 모델을 사용해야 함)
    following = models.ManyToManyField(
        'self',
        related_name='follower_set',
        symmetrical=False,
        through='Relationship',
    )

    is_staff = models.BooleanField(default=False)

    img_profile = models.ImageField(upload_to='user', blank=True)

    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    # 메서드 추가
    # MyUser를 팔로우 (자신의 following 목록에 추가)
    def follow(self, user):
        self.following_relations.create(
            to_user=user
        )

    def unfollow(self, user):
        self.following_relations.filter(
            to_user=user
        ).delete()

    def get_full_name(self):
        return '{} {}'.format(
            self.nickname,
            self.username
        )

    def get_short_name(self):
        return self.nickname


class Relationship(models.Model):
    from_user = models.ForeignKey(MyUser, related_name='following_relations')
    to_user = models.ForeignKey(MyUser, related_name='follower_relations')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user')
        )

    def __str__(self):
        return 'Relation from {} to {}'.format(
            self.from_user.username,
            self.to_user.username,
        )
