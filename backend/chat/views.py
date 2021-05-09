from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponseRedirect
# Create your views here.

@login_required
def room(request, room_name):
    
    return render(request, 'chat/chat.html', {
        'room_name': room_name,
        'username': request.user.username,
        'user': request.user,
    })

def get_last_10_messages(chatId):
    try:
        chat = get_object_or_404(Chat, code_for_chat=chatId)
        return chat.messages.order_by('-timestamp').all()[:10]
    except:
        return '0'

def get_current_chat(chatId):
    try:
        return get_object_or_404(Chat, code_for_chat=chatId)
    except:
        return '0'
