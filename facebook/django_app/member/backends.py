import os
import re

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from member.models import MyUser


# 시나리오가 두 가지
# 1. 페이스북 로그인 버튼을 누르면 바로 서비스 시작
# 2. 추가 정보가 꼭 있어야 된다고하면(가령, 핸펀 번호 등),
# 사용자 정보를 받고나서, 회원가입화면으로 다시 가서
# authentication 을 하는 루틴
class FacebookBackend():
    # facebook_id가 주어졌을 때, 해당 user가 있으면 가져오고,
    # 없으면 user를 만들어서 return 해 주는 인증 과정을 구현한 상태.
    def authenticate(self, facebook_id, extra_fields):
        url_profile = 'http://graph.facebook.com/{user_id}/picture'.format(
            user_id=facebook_id
        )
        params = {
            'type': 'large',
            'height': '500',
            'width': '500',
        }

        # Image 파일을 저장하기 위해 임시로 메모리에 파일을 생성한 다음에,
        # 우리의 이미지 필드에 저장한다.(1~6)

        # 1. 메모리상에 임시파일 생성
        temp_file = NamedTemporaryFile(delete=False)
        # 2. 프로필 이미지의 URL에 get요청, stream에 True지정
        # (strem=True로 지정하면 조각단위로 받는 방식)
        r = requests.get(url_profile, params, stream=True)
        print(r.url)
        # 3. 요청하는 URL에서 파일 확장자를 가져옴(splitext:확장자와 이름을 구분)
        # 근데, '.'의 앞과 뒤만 구분만 해주기 때문에, '.'뒤에 확장자와 parameters가 붙어서 같이오기 때문에,
        # 추가로 정규식 표현으로 분리를 해야함
        _, file_ext = os.path.splitext(r.url)
        print('front: %s' % _)
        print('back: %s' % file_ext)

        # '\1'은 첫번째 matching 되는 그룹: ()안에 있는 것을 의미.
        # '.'으로 시작하는데 ?는 제외하고 반복
        file_ext = re.sub(r'(\.[^?]+).*', r'\1', file_ext)
        print(file_ext)
        # 4. 페이스북 유저 ID.확장자 로 file_name을 지정
        file_name = '{}{}'.format(
            facebook_id,
            file_ext
        )
        # 5. stream으로 연결된 response에서 1024bytes단위로 데이터를 받아 임시파일에 기록
        for chunk in r.iter_content(1024):
            temp_file.write(chunk)

        # facebook_id가 username인 MyUser를 갖고오거나
        # defaults값을 이용해서 생성
        defaults = {
            'first_name': extra_fields.get('first_name', ''),
            'last_name': extra_fields.get('last_name', ''),
            'email': extra_fields.get('email', ''),
        }

        # 만약 get 하는 데 실패하면, user를 만들어 주자.
        # 실패했을 때, user를 만드는 간단한 방법 : get_or_create
        # user = MyUser.objects.get(username=facebook_id)
        user, user_created = MyUser.objects.get_or_create(
            defaults=defaults,
            username=facebook_id,
        )
        print(user)

        # 6. ImageField의 save메서드에 파일명과 Django에서 지원하는 File객체를 전달
        # 파일 필드에 우리가 임시로 만든 파일을 저장하려면, user를 create하는 과정에서는 저장할 수가 없다.
        # 그래서, create 한 다음에 해당 필드에서 save를 눌러줘야 함.
        # img_profile는 ImageField 인데, ImageField에 있는 save 메소드가 따로 있어서 이걸 이용함.
        # 그리고, 이 임시 파일을 장고에서 지원하는 File 객체로 한 번 더 감싸 준 다음에 전달해주어야 한다.
        user.img_profile.save(file_name, File(temp_file))
        return user

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None
