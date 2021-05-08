from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',jobList.as_view(),name='job-list'),
    path('explore/',allJob.as_view(),name='job-explore'),
    path('create/',jobCreate.as_view(),name='job-create'),
    path('detail/<int:pk>',jobDetail.as_view(),name='job-detail'),
    path('update/<int:pk>',jobUpdate.as_view(),name='job-update'),
    path('apply/<int:pk>',apply,name='job-apply'),
    path('dashboard/',dash,name='job-dash'),
    path('dashboard/list/',jobdashlist.as_view(),name='job-dash-list'),
    path('dashboard/job/<int:pk>',viewpeople.as_view(),name='job-dash-detail'),

]