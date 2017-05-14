from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hot$', views.hot, name='hot'),
    url(r'^tag/(?P<tag_name>.+)$', views.tag, name='tag'),
    url(r'^ask$', views.ask, name='ask'),
    url(r'^question/(?P<question_id>\d+)$', views.question, name='question'),
    url(r'^question/(?P<question_id>\d+)/like$', views.question_like, name='question_like'),
    url(r'^answer/(?P<answer_id>\d+)/like$', views.answer_like, name='answer_like'),
    url(r'^login$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^settings$', views.settings, name='settings'),
    url(r'^hello_world$', views.hello_world),
]