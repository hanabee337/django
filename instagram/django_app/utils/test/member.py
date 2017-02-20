from member.models import MyUser

__all__ = (
    'make_dummy_users',
)


def make_dummy_users():
    users = []

    for i in range(10):
        user = MyUser.objects.create(
            username='username{}'.format(i + 1),
            password='test_password'
        )
        users.append(user)
    return users
