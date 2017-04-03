from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ask', views.ask, name='ask'),
    url(r'^question', views.question, name='question'),
]