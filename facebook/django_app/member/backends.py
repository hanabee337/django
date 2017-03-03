from member.models import MyUser


# 시나리오가 두 가지
# 1. 페이스북 로그인 버튼을 누르면 바로 서비스 시작
# 2. 추가 정보가 꼭 있어야 된다고하면(가령, 핸펀 번호 등),
# 사용자 정보를 받고나서, 회원가입화면으로 다시 가서
# authentication 을 하는 루틴
class FacebookBackend():
    # facebook_id가 주어졌을 때, 해당 user가 있으면 가져오고,
    # 없으면 user를 만들어서 return 해 주는 인증 과정을 구현한 상태.
    def authenticate(self, facebook_id, **extra_fields):
        # 만약 get 하는 데 실패하면, user를 만들어 주자.
        # 실패했을 때, user를 만드는 간단한 방법 : get_or_create
        # user = MyUser.objects.get(username=facebook_id)
        user, user_created = MyUser.objects.get_or_create(
            username=facebook_id
        )
        return user

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None
