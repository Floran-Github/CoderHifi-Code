from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'chat/chatindex.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

 # def connect(self):
    #     self.room_name = self.scope['url_route']['kwargs']['room_name']
    #     self.room_group_name = 'chat_%s' % self.room_name
    #     async_to_sync(self.channel_layer.group_add)(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #     self.accept()

    # # def connect(self):
    # #     self.room_name = self.scope['url_route']['kwargs']['room_name']
    # #     self.room_group_name = 'chat_%s' % self.room_name

    # #     # Join room group
    # #     async_to_sync(self.channel_layer.group_add)(
    # #         self.room_group_name,
    # #         self.channel_name
    # #     )

    # #     self.accept()

    # def disconnect(self, close_code):
    #     async_to_sync(self.channel_layer.group_discard)(
    #         self.room_group_name,
    #         self.channel_name
    #     )

    # def receive(self, text_data):
    #     data = json.loads(text_data)
    #     print('receive')
    #     self.commands[data['command']](self, data)

    # def send_msg(self,message):

    #     # Send message to room group
    #     async_to_sync( self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

    # # Receive message from room group
    # def chat_message(self, event):
    #     message = event['message']

    #     # Send message to WebSocket
    #     async_to_sync( self.send(text_data=json.dumps({
    #         'message': message
    #     })))
    # commands = {
    #     'fetch_messages': fetch_messages,
    #     'new_message': new_message
    # }