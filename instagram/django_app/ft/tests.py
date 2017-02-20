from django.test import LiveServerTestCase
from django.utils.crypto import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from member.models import MyUser
from post.models import Post
from utils.test import make_dummy_users


class BaseTestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(30)

    def tearDown(self):
        self.browser.quit()

    def make_url(self, url):
        result = '{}{}'.format(self.live_server_url, url)
        return result

    def make_user_and_login(self):
        # 임의의 유저를 생성
        test_username = 'test_username'
        test_password = 'test_password'
        user = MyUser.objects.create_user(test_username, test_password)

        # 유저를 강제로 로그인 시킴
        self.browser.get(self.make_url('/member/login/'))
        input_username = self.browser.find_element_by_id('id_username')
        input_username.send_keys(test_username)
        input_password = self.browser.find_element_by_id('id_password')
        input_password.send_keys(test_password)
        input_password.send_keys(Keys.ENTER)

        return user


class NewVisitorTest(BaseTestCase):
    # 로그인하진 않은 유저가 member:signup으로 잘 이동했는지 확인
    def test_first_visitor_redirect_to_signup(self):
        self.browser.get(self.live_server_url)
        self.assertEqual(self.make_url('/member/signup/'), self.browser.current_url)

    # 로그인 한 유저가 post:list로 잘 이동했는지 확인
    def test_logged_in_user_redirect_to_post(self):
        self.make_user_and_login()

        # 이후 다시 root url을 요청
        self.browser.get(self.live_server_url)
        # self.assertEqual(self.live_server_url + '/post/', self.browser.current_url)
        self.assertEqual(self.make_url('/post/'), self.browser.current_url)


class ProfileTest(BaseTestCase):
    """
    프로필 페이지에서의 동작을 테스트한다.
    """

    def access_profile_page_and_check_status(self, status_name, unit, num):
        # 프로필 페이지에 접근
        self.browser.get(self.make_url('/member/profile/'))
        page_text = self.browser.find_element_by_tag_name('body').text

        # 현재 게시물/팔로우/팔로워한 인원이 정상적으로 표시되는지 확인
        self.assertIn(
            '{status_name} {num}{unit}'.format(
                status_name=status_name,
                num=num,
                unit=unit
            ),
            page_text
        )

    def test_profile_display_status_post_count(self):
        # 테스트 할 유저 생성
        user = self.make_user_and_login()
        num = random.randrange(1, 10)
        # 임의의 유저 생성
        for i in range(num):
            Post.objects.create(
                author=user,
            )

        # 생성한 게시불 수가 정상적으로 표시되는지 확인
        self.access_profile_page_and_check_status(status_name='게시물', unit='개', num=num)

    def test_profile_display_status_follower_count(self):
        user = self.make_user_and_login()
        users = make_dummy_users()

        num = random.randrange(1, 10)
        for i in range(num):
            users[i].follow(user)

        self.access_profile_page_and_check_status(status_name='팔로워', unit='명', num=num)

    def test_profile_display_status_following_count(self):
        user = self.make_user_and_login()
        users = make_dummy_users()

        num = random.randrange(1, 10)
        for i in range(num):
            user.follow(users[i])

        self.access_profile_page_and_check_status(status_name='팔로우', unit='명', num=num)
