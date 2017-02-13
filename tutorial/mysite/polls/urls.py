from django.conf.urls import url

from . import views

# part3, URL의 이름공간(namespace) 나누기
app_name = 'polls'

# Part 4 : URLconf 수정
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),        
]


"""
urlpatterns = [
        # ex: /polls/
        url(r'^$', views.index, name='index'),
        # ex: /polls/5/
        url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
       
        # part3, Template 에서 하드코딩된 URL 을 제거하기
        # added the word 'specifics'
        #url(r'^specifics/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
        
        # ex: /polls/5/results/
        url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
        # ex: /polls/5/vote/
        url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]
"""


