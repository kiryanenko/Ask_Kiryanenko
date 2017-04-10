from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ask', views.ask, name='ask'),
    url(r'^question', views.question, name='question'),
    url(r'^login', views.login, name='login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^hello_world', views.hello_world),
]