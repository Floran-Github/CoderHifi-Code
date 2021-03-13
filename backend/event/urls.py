from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',eventListView.as_view(),name='event-list'),
    path('dashboard/',event_dashboard,name='event-dashboard'),
    path('dashboard/list/',event_list_dashboard,name='event-dashboard-list'),
    path('dashboard/add/<int:pk>/',add_participant_event_list,name='event-add-participant'),
    path('dashboard/add/participant/<int:pk>/',add_participant,name='event-add'),
    path('create/',eventCreateView.as_view(),name='event-create'),
    path('update/<int:pk>',eventUpdateView.as_view(),name='event-update'),
    path('delete/<int:pk>',eventDeleteView.as_view(),name='event-delete'),
    path('enroll/<int:pk>',enroll,name='event-enroll'),

    
]