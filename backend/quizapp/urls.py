from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',MainQuizList.as_view(),name = 'courses'),
    path('detail/<int:pk>',quizLevel.as_view(),name = 'quiz_level'),
    path('detail/<int:pk>/quiz',index,name = 'quiz'),
    path('check',getanswer,name = 'get_ans'),
    path('create/question',createPage,name = 'create_page'),
    path('create',createquiz,name = 'create'),

]