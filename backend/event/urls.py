from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',eventListView.as_view(),name='event-list'),
    path('dashboard/',event_dashboard,name='event-dashboard'),
    path('create/',eventCreateView.as_view(),name='event-create'),
    path('update/<int:pk>',eventUpdateView.as_view(),name='event-update'),
    path('delete/<int:pk>',eventDeleteView.as_view(),name='event-delete'),
    path('enroll/<int:pk>',enroll,name='event-enroll'),

    
]