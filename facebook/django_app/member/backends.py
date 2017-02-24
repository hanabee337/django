import requests

from member.models import MyUser


class FacebookBackend():
    def authenticate(self, facebook_id, **extra_fields):
        # url_profile = ''
        # params = {
        #     'type': 'large',
        #     'width':'500',
        #     'height':'500',
        # }
        # r = requests.get(url_profile, params, stream=)

        defaults = {
            'first_name': extra_fields.get('first_name'),
            'last_name': extra_fields.get('last_name'),
            'email': extra_fields.get('email'),
        }
        user, user_created = MyUser.objects.get_or_create(
            username=facebook_id
        )
        return user

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None
