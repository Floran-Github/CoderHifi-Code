from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',MainQuizList.as_view(),name = 'courses'),
    path('detail/<int:pk>',quizLevel.as_view(),name = 'quiz_level'),
    path('detail/<int:pk>/quiz',ActualQuiz.as_view(),name = 'quiz'),
]