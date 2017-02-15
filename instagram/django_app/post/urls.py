from django.conf.urls import url

from . import views

app_name = 'post'
urlpatterns = [
    url(r'^post$/', views.post_list, name='post_list'),

    url(r'^post/(?P<post_id>[0-9]+)/', views.post_detail, name='post_detail')
]
