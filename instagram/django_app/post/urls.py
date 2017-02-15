from django.conf.urls import url

from . import views

app_name = 'post'
urlpatterns = [
    url(r'^post/', views.post_list, name='post_list')
]
