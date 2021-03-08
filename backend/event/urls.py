from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',eventListView.as_view(),name='event-list'),
    path('create/',eventCreateView.as_view(),name='event-create'),
    path('update/<int:pk>',eventUpdateView.as_view(),name='event-update'),
    path('delete/<int:pk>',eventDeleteView.as_view(),name='event-delete'),
    
]