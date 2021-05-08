from django.urls import path

from . import views

urlpatterns = [
    path('',views.get_room,name='chat'),
    path('public/',views.get_public_room,name='public-chat'),
    path('student/<int:pk>',views.chat_with_Student,name='teacher-chat'),
    path('<str:room_name>/', views.room, name='room'),
]