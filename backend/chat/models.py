from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
import os 
# Create your models here.
class PublicChatRoom(models.Model):
    room_name = models.CharField(max_length=100,unique=True)
    users = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return self.room_name

    def connect_user(self,user):
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect(self,user):
        is_user_removed = False
        if not user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed


    @property
    def group_name(self):
       
        return f'PublicChatRoom-{self.id}'

class PublicChatManager(models.Manager):

    def by_room(self,room):
        qs = PublicChatMsg.objects.filter(room=room).order_by("-time")
        return qs

class PublicChatMsg(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    objects = PublicChatManager()
    def __str__(self):
        return self.content

class message(models.Model):
    user = models.ForeignKey(User,related_name='user_message',on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def recent_message(self):
        return message.objects.order_by('-timestamp').all()[:10]



