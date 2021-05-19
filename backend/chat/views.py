from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from course.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.


def get_room(request):
    courseId = request.session.get('fxfrd')
    room_code = Chat.objects.filter(course=courseId,user_in_chat=request.user)
    if request.user.is_staff:
        for i in room_code:
            # print(i.code_for_chat)
            students = i.course.studentEnrolled.all()
            return render(request,'chat/studentList.html',context={'objects':students})
    else:
        # print(room_code.code_for_chat)
        return redirect('room',room_name=room_code[0].code_for_chat)

def chat_with_Student(request,pk):
    print('in funt')
    courseId = request.session.get('fxfrd')
    room_code = Chat.objects.filter(course=courseId,user_in_chat=User.objects.get(id=pk))
    return redirect('room',room_name=room_code[0].code_for_chat)

def get_public_room(request):
    courseId = request.session.get('fxfrd')
    courses = get_object_or_404(course,pk=courseId)
    print(courses)
    room_code = PublicChat.objects.filter(course=courses)
    print('public - ',courseId)
    return redirect('room',room_name=room_code[0].code_for_chat)

@login_required
def room(request, room_name):
    
    return render(request, 'chat/chat_template.html', {
        'room_name': room_name,
        'username': request.user.username,
        'user': request.user,
    })

def get_last_10_messages(chatId):
    try:
        chat = get_object_or_404(Chat, code_for_chat=chatId)
        return chat.messages.order_by('timestamp').all()[:10]
    except:
        chat = get_object_or_404(PublicChat, code_for_chat=chatId)
        return chat.messages.order_by('timestamp').all()[:10]

def get_current_chat(chatId):
    try:
        return get_object_or_404(Chat, code_for_chat=chatId)
    except:
        return get_object_or_404(PublicChat, code_for_chat=chatId)
