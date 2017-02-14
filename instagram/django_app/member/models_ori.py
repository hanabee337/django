from django.db import models, IntegrityError


class MyUser(models.Model):
    username = models.CharField(max_length=30, unique=True)
    last_name = models.CharField('성', max_length=20)
    first_name = models.CharField('이름', max_length=20)
    nickname = models.CharField('닉네임', max_length=24)
    email = models.EmailField('이메일', blank=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)
    following = models.ManyToManyField(
        'self',
        related_name='follower_set',
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.username

    def follow(self, user):
        self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)

    # 마음대로 수정못하게 읽기전용으로
    @property
    def followers(self):
        return self.follower_set.all()

    def change_nickname(self, new_nickname):
        self.nickname = new_nickname
        self.save()

    @staticmethod
    def create_dummy_user(num):
        """
        num개수 만큼 User1 ~ User<num>까지 임의의 유저를 생성한다
        :return: 생선된 유저 수
        """
        import random
        last_name_list = ['박', '신', '김', '정', '송', '이', '백']
        first_name_list = ['보현', '준성', '은별', '재희', '선아', '다희', '민주', '규원']
        nickname_list = ['찬이맘', '아재', '세글자', '티부', '해방촌가수']
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

    # 자동으로 변수에 할당해주는 메소드를 만들었다!!!
    @staticmethod
    def assign_global_variables():
        # sys모듈은 파이썬 인터프리터 관련 내장 모듈
        import sys
        # __main__모듈을 module변수에 할당
        module = sys.modules['__main__']
        # MyUser객체 중 'User'로 시작하는 객체들만 조회하여 user변수에 할당
        users = MyUser.objects.filter(username__startswith='User')
        # users를 순회하며
        for index, user in enumerate(users):
            # __main__모듈에 u1,u2,u3... 이름으로 각 MyUser객체를 할당
            setattr(module, 'u{}'.format(index + 1), user)
