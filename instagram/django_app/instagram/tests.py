from django.test import Client
from django.test import LiveServerTestCase

from member.models import MyUser

"""
Mission  # 2 - 테스트 작성(TDD 배운 걸로)
1. index URL로 접근했을 때, 로그인하지 않았을 경우, member: signup을 가는지 확인
"""

class IndexTest(LiveServerTestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_user_is_not_authenticated_redirect_to_signup(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/member/signup/')

    def test_user_is_authenticated_redirect_to_post_list(self):
        """
        유저를 로그인 시킨다.
        # 테스트용 유저를 생성한다.(ORM)
        # member:login 으로 POST요청을 보낸다.(self.client.post)
        이후, root url('/')의 response를 받아온다.
        해당 response가 /post/로 잘 redirect되는지 확인
        :return:
        """
        test_username = 'test_user'
        test_password = 'test_password'
        MyUser.objects.create_user(test_username, test_password)

        # member:login으로 POST 요청을 보낸다(self.client.post)
        self.client.post(
            '/member/login/',
            {
                'username': test_username,
                'password': test_password
            }
        )

        # 다시 root URL의 response를 받아와
        response = self.client.get('/')
        # 해당 response가 /post/로 redirect 되는지 확인
        self.assertRedirects(response, '/post/')
