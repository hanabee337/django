"""
1. 모델을 정의
2. 모델이 속한 app을 settings.py의 INSTALLED_APPS에 등록
3. 등록 후 해당 app의 모델을 데이터베이스에 적용시키기위해 makemigrations -> migrate
4. 장고 어드민에 등록시킬 모델을 admin.py에 admin.site.register(모델명)으로 등록
5. 장고 어드민에 로그인 하기위해 ./manage.py createsuperuser로 관리자계정 생성
6. runserver후 localhost:8000/admin으로 접속해서 해당 계정으로 로그인
7. person앱의 Person테이블이 잘 보이는지 확인
"""
from django.db import models


# ManyToOne
class Person(models.Model):
    SHIRT_SIZE = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )

    name = models.CharField('이름', max_length=60, help_text='성과 이름을 붙여 적으세요')
    shirt_size = models.CharField('셔츠 사이즈', max_length=1, choices=SHIRT_SIZE, default=SHIRT_SIZE[0][0])
    nationality = models.CharField('국적', max_length=200, default='South Korea')

    # To create a recursive relationship
    # – an object that has a many-to-one relationship with itself
    # – use models.ForeignKey('self', on_delete=models.CASCADE).
    # 외래키 관계를 자기 자신의 클래스에 갖는 경우
    # One-To-Many에선 One이 사라지게 되면, Many도 같이 가라지게 됨.
    # 즉, 기본 설정이 on_delete=models.CASCADE, 이렇게 되어 있다는 의미. 같이 지워진다는 의미.
    instructor = models.ForeignKey('self', verbose_name='담당 강사', null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name='student_set')

    owner = models.ForeignKey(
        'self',
        verbose_name='사장님',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        # mentor랑 owner가 related_name이 모두 없으면,
        # makemigrations할 때, 에러가 발생한다.
        # 그래서, related_name으로 명시를 해줘야 한다.
        # 다음과 같이 서로 역참조해서 에러가 난다고 함.
        # person.Person.mentor: (fields.E304) Reverse accessor
        # for 'Person.mentor' clashes with reverse accessor for 'Person.owner'.

        related_name='employee_set',
    )

    mentor = models.ForeignKey(
        'self',
        verbose_name='멘토',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='mentee_set',
    )

    def __str__(self):
        return self.name


# ManyToMany
class User(models.Model):
    # 팔로우 팔로잉 관계를 나타낼땐, symmetriacal=False로 설정 가능
    followers = models.ManyToManyField(
        'self',
        related_name='following_set',
        symmetrical=False,
    )
    # following = models.ManyToManyField(
    #     'self',
    #     related_name='follower_set',
    #     symmetrical=False,
    # )

    # 단순 친구 관계를 나타낼 때는
    # 한 객체가 다른 객체를 /친구/로 선언하면
    # 반대쪽에서도 자동으로 '친구'로 설정됨
    # 이 경우는 기본 값(symetrical=True)
    #
    # 그런데, 만약, 친구관계에 대한 추가정보가 필요할 경우,
    # through를 통해서 중간자 모델을 참조함
    #
    # 중간자 모델을 사용할 경우에는
    # symmetrical이 반드시 False이어야 함.
    # 이 경우 양쪽이 동시에 친구관계를 맺고자 하면ㅡ
    # 두 관계를 한 번에 생성해주는 메서드를 생성해 사용해야 함.
    #
    #
    #
    # 친구관계에 대한  추가정보 중간자 모델이
    # 친구관계를 나타내는 User ForeignKey를 두 개 초과해서
    # 가질 경우, 어떤 User ForeignKey로(2개)가 관계를 나타내야 하는지를 위해
    # through_fields로 알려주어야 함.
    following = models.ManyToManyField(
        'self',
        # through='UserFriendsInfo',
        # through_fields=('from_user', 'to_user'),
        # symmetrical=False,
    )

    friends = models.ManyToManyField('self')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserFriendsInfo(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='+',
    )

    to_user = models.ForeignKey(
        User,
        related_name='+',
    )

    # 중개인이라는 User ForeignKey가 추가로 존재할 경우,
    # 중간자 모델을 사용하는 곳에서 through_fields를 정의해야 함
    recommender = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='recommender_userfriendsinfo_set'
    )

    when = models.DateTimeField(auto_now_add=True)


# Extra fields on many-to-many relationships
# 서로 다른 모델간의 MTM에서, 중간자 모델을 사용하는 ㄱ경우
class Idol(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)
    member = models.ManyToManyField(
        Idol,
        # 두 관계를 정의하는 중간자 모델을 지정
        through='Membership',
        # 이건 기본값이며, 만약 중간자 모델에서 관계를 형성하는 두 클래스 중
        # 한 클래스라도 한 번을 초과하여 필드로 사용될 걍우
        # through_fields에 내용을 적어야 한다.
        #             ( from ,   to   )
        through_fields=('group', 'idol'),
    )

    def __str__(self):
        return self.name


# membership 클래스가 중간자 모델이 된다.
# idol 과  group 사이의 테이블을 만든다.
# 중간자 모델이 되려면 명시적으로 외래키로 선언해 주어야 한다.
class Membership(models.Model):
    idol = models.ForeignKey(Idol)
    group = models.ForeignKey(Group)

    # 아래 처럼 Idol을 idol = models.ForeignKey(Idol)랑 같이 외래키로 선언할 수 없다.
    # 한 개씩만 가질 수 있다.
    # recommender = models.ForeignKey(Idol)
    # idol, recommender 이렇게 두개가 있으면,
    # 중간자 모델은 어떻게  through 시켜야 하는지 모른다.
    # 추천인이라는 Target 모델에 대한 추가 피ㄹ드가 있을 경우,
    # 이 경우에도 through_fields를 정의해줘ㅇ야 함
    date_joined = models.DateTimeField()
    recommender = models.ForeignKey(
        Idol,
        null=True,
        blank=True,
        related_name='recommender_membership_set'
    )

    def __str__(self):
        return '{} - {} {}'.format(
            self.group.name,
            self.idol.name,
            self.date_joined,
        )
