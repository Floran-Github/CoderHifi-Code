from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',mainpage,name='mainpage'),
    path('dev/',devpage,name='devpage'),
    path('rec',recpage,name='recpage'),
]