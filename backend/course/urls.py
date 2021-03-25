from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',courseListView.as_view(),name='course-list'),
    path('create/',courseCreateView.as_view(),name='course-create'),
    path('detail/<int:pk>/',courseDetailView.as_view(),name='course-detail'),
    
]