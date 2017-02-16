from django.conf.urls import url

from . import views

app_name = 'post'
urlpatterns = [
    url(r'^post/$', views.post_list, name='post_list'),

    url(r'^post/(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),

    url(r'^post/(?P<post_id>[0-9]+)/comment/add/$', views.comment_add, name='comment_add'),

    url(r'^post/(?P<post_id>[0-9]+)/like/toggle/$', views.post_like_toggle, name='like_toggle'),

]
