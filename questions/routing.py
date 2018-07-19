from django.conf.urls import url

from questions import consumers

websocket_urlpatterns = [
    url(r'^questions/(?P<question_id>[^/]+)/$', consumers.QuestionConsumer),
]