# 1. Post모델 구현(like_users빼고)
#     pip install Pillow
# 2. PostLike 모델 구현 (중간자 모델로 구현)
# 3. Post모델의 like_users 필드 구현
# 4. Comments 모델 구현

from django.db import models

from member.models import MyUser


class Post(models.Model):
    author = models.ForeignKey(MyUser)
    photo = models.ImageField(
        upload_to='post', blank=True
    )
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # user와 post사이에 manytomany를 설정하는데,
    # post가 user쪽에 영향을 행사하는게 아니고,
    # user가 post쪽에 영향을 주니까, 여기에서 설정
    like_users = models.ManyToManyField(
        MyUser,
        blank=True,
        through='PostLike',
        # 역참조는 언제쓰나? user에서 post로 갈 때,
        # 내가 like를 했던 post의 set을 가져오고 싶다할 때, 역참조 가능하다.
        related_name='like_post_set',
    )

    def __str__(self):
        return 'Post{}'.format(self.id)

    def add_comment(self, user, content):
        # 자신에게 연결된 comment객체의 역참조 매니저(comment_set)로부터
        # create 메서드를 이용해 Comment 객체를 생성
        # Comment.objectes.create(
        #     post=self,
        #     user = user,
        #     content=content
        # )
        # 위처럼 만들 수도 있지만, 역참조하는 매니저를 가지고 만들 수 있다.
        # self 인스턴스 자체가 지금 post 인스턴스이기 때문에
        # 이쪽에서 역참조해서 만드는 것이 맞다..
        # 이렇게 하면 Post의 인자를 넣을 필요가 없다.
        # self 자체가 Post가 들어가니까, self의 comment_set에서 만들기 때문에
        # Post는 안넣어도 된다.
        return self.comment_set.create(
            author=user,
            content=content
        )

    @property
    def like_count(self):
        # pass
        return self.like_users.count()

    @property
    def comment_count(self):
        return self.comment_set.count()

    def toggle_like(self, user):
        # PostLike 중간자 모델에서 인자로 전달된 Post,Myuser 객체를 가진 row를 조회
        # pl_list = Post.objects.filter(post=self, user=user)
        # 윗줄 보다 아랫줄이 더 직관적
        pl_list = self.postlike_user_set.filter(user=user)

        # 1. 현재 인자로 전달된 user가 해당 Post(self)를 좋아요 한 적이 있는지
        # if pl_list.exist():
        # if self.like_users.filter(id=user.id).exists():
        # 2. 만약 이미 좋아요를 했을 경우 해당 내역을 삭제
            # 중간자 모델을 사용했으므로 self.like_users.remove(user)로 직접 삭제 불가
            # 그래서, 아래 메서드를 사용함.
            # self.like_users.remove(user)
            # PostLike.objects.filter(post=self, user=user)
            # pl_list.delete()
        # 3. 아직 내영기 없을 경우, 생성해 준다.
        # else :
            # 중간자 모델을 사용했으므로 self.like_users.create(user)로 직접 생성 불가,
            # 대신에 PostLike 중간자 모델 매니저를 사용한다.
            # self.like_users.create(user)
            # PostLike.objects.create(post=self, user=user)


        # if pl_list.exist():
            # pl_list.delete()
        # else :
            # PostLike.objects.create(post=self, user=user)
        # 위의 조건문을 한 줄로 줄이면
        # 파이썬 삼항연산자
         # [True일 경우 실행할 구문] if 조건문 else [False일 경우 실행할 구문]
        return PostLike.objects.create(post=self, user=user) \
            if not pl_list.exists() else pl_list.delete()


class PostLike(models.Model):
    user = models.ForeignKey(MyUser)
    post = models.ForeignKey(Post)
    created_date = models.DateTimeField(auto_now_add=True)

    # self.post.id vs self.post_id
    # post.id는  테이블까지 join을 시킨 다음에 데이터를 가져오는데,
    # post_id 는 거기까지 안간다. db table이 이미 만들어져 있다.
    def __str__(self):
        return 'Post[{}]\'s Like[{}, Author[{}]'.format(
            self.post_id,
            self.id,
            self.post.author,
        )

    # 한 유저가 좋아요를 두 번 눌러도 중복이 되지 않게 하기 위해.
    class Meta:
        unique_together = (
            ('user', 'post')
        )


class Comment(models.Model):
    author = models.ForeignKey(MyUser)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post[{}]\'s Comment[{}], Author[{}]'.format(
            self.post_id,
            self.id,
            self.author_id,
        )
