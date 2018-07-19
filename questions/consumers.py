import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class QuestionConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.question_id = self.scope['url_route']['kwargs']['question_id']
        self.room_group_name = 'question_%s' % self.question_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def new_answer(self, answer):
        self.send_json(answer)
