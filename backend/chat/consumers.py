import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import User
from .models import *
class ChatConsumer(WebsocketConsumer):

    def fetch_msg(self,data):
        print('fetch')
        msgs = message.recent_message()
        content = {
            'messages': self.messages_to_json(msgs)
        }
        self.send_message(content)
        pass

    def new_msg(self,data):
        print('yo')
        user = data['from']
        user_data = User.objects.filter(username=user)[0]
        message = message.objects.create(user=user_data,message=data['message'])
        connect = {
            'commmand': 'new_messages',
            'message' : self.message_to_json()
        }
        return self.send_chat_message(content)
        pass

    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self,message):
        return {
            'author' : message.user.username,
            'content' : message.message,
            'timestamp' : str(message.timestamp)
        }

    commands = {
        'fetch_messages' : fetch_msg,
        'new_messages' : new_msg,
    }
   

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


    def send_chat_message(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

 
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))