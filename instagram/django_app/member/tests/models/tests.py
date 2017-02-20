from django.db import IntegrityError
from django.test import TransactionTestCase

from utils.test import make_dummy_users

"""
dummy 유저를 여러명 만들어서 서로 팔로워/팔로잉 관계를 갖도록 테스트
"""


class MyUserModelTest(TransactionTestCase):
    def test_following(self):
        users = make_dummy_users()

        # 임의의 유저가 다른 유저를 follow
        # 0은 123을 팔로우
        users[0].follow(users[1])
        users[0].follow(users[2])
        users[0].follow(users[3])

        users[1].follow(users[2])
        users[1].follow(users[3])

        users[2].follow(users[3])

        self.assertIn(users[1], users[0].following.all())
        self.assertIn(users[2], users[0].following.all())
        self.assertIn(users[3], users[0].following.all())

        self.assertIn(users[2], users[1].following.all())
        self.assertIn(users[3], users[1].following.all())

        self.assertIn(users[3], users[2].following.all())

        # 반대로 follower를 가진 유저는 follower_set 역참조 이름으로
        # follow하는 유저를 출력하는지 확인
        self.assertIn(users[0], users[3].follower_set.all())
        self.assertIn(users[1], users[3].follower_set.all())
        self.assertIn(users[2], users[3].follower_set.all())

        self.assertIn(users[0], users[2].follower_set.all())
        self.assertIn(users[1], users[2].follower_set.all())

        self.assertIn(users[0], users[1].follower_set.all())

    def test_following_duplicate(self):
        users = make_dummy_users()
        users[0].follow(users[1])

        # 중복 팔로우 시도
        # users[0].follow(users[1])
        # users[0].follow(users[1])

        # 중복 팔로우 시도, Integrity Error 발생과 함께
        # 실패함을 확인
        with self.assertRaises(IntegrityError):
            users[0].follow(users[1])

        # 중복으로 팔로우 했어도 실제로는 하나만 남아있어야 함.
        self.assertEqual(users[0].following.count(), 1)
        self.assertEqual(users[1].follower_set.count(), 1)

    def test_unfollow(self):
        users = make_dummy_users()

        users[0].follow(users[1])
        users[0].follow(users[2])
        users[0].follow(users[3])

        users[0].unfollow(users[1])
        self.assertEqual(users[0].following.count(), 2)

        users[0].unfollow(users[2])
        self.assertEqual(users[0].following.count(), 1)

        users[0].unfollow(users[3])
        self.assertEqual(users[0].following.count(), 0)


