from django.db import models, IntegrityError


# from django.contrib.auth import

# Create your models here.

class MyUser(models.Model):
    username = models.CharField('유저네임', max_length=200,
                                unique=True)
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    nickname = models.CharField('닉네임', max_length=24)
    email = models.EmailField('이메일', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    following = models.ManyToManyField(
        'self',
        related_name='follower_set',
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.username

    # shell에서 일일이 작업하는 게 귀찮으니...
    @staticmethod
    def create_dummy_user(num):
        """
        num 갯수만큼 User1~User<num>까지 임의의 유저를 생성한다.
        :return: 생성된 유저 수
        """
        import random
        last_name_list = ['방', '이', '김', '최']
        first_name_list = ['민아', '혜리', '수아', '소영']
        nickname_list = ['만득', '노랭', '우렁', '근덕']
        created_count = 0

        for i in range(num):
            try:
                MyUser.objects.create(
                    username='User{}'.format(i + 1),
                    last_name=random.choice(last_name_list),
                    first_name=random.choice(first_name_list),
                    nickname=random.choice(nickname_list),
                )
                created_count += 1
            except IntegrityError as e:
                print(e)

        return created_count

    def follow(self, user):
        self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)

    @property
    def followers(self):
        # 자신을 following 하는 모든 목록을 리턴
        return self.follower_set.all()

    def change_nickname(self, new_nickname):
        self.nickname = new_nickname
        self.save()

    # shell에서 u1 = MyUser.objects.get(id=1)을 일일이 작업하는 게 귀찮으니...
    @staticmethod
    def assign_global_variables():
        # interpreter를 다루는 부분
        # sys모듈은 python 인터프리터 관련 내장 모듈
        import sys

        # __main__ 모듈을 module변수에 할당
        # shell에서 입력한 global 변수와 같은 역할
        module = sys.modules['__main__']
        # MyUser 객체 중 'User'로 시작하는 객체들만 조회하여 users변수에 할당
        users = MyUser.objects.filter(username__startswith='User')
        # users를 순회하며
        for index, user in enumerate(users):
            # __main__ 모듈에 'u1,u2,u3 ...." 이름으로 각 MyUser객체를 할당
            setattr(module, 'u{}'.format(index + 1), user)


