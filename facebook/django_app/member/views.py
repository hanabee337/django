from django.shortcuts import render

from facebook import settings


def login_fbv(request):
    print('login_fbv')
    facebook_app_id = settings.config['facebook']['app_id']
    context = {
        'facebook_app_id': facebook_app_id,
    }
    return render(request, 'member/login.html', context)


def login_facebook(request):
    print(request.GET)
