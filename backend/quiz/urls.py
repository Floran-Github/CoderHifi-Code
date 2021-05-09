from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',MainQuizList.as_view(),name = 'courses'),
    path('detail/<int:pk>',quizLevel.as_view(),name = 'quiz_level'),
    path('detail/<int:pk>/quiz',index,name = 'quiz'),
    path('quiz/zaki/',getanswer,name = 'get_ans'),
    path('detail/<int:pk>/save_ans/',save_ans,name="saveans"),
    path('detail/<int:pk>/result/',result,name="result"),
    path('detail/',welcome,name='quiz_level'),

]