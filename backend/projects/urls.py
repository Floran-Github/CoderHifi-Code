from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',projectListView.as_view(),name='project-list'),
    path('create/',projectCreateView.as_view(),name='project-create'),
    path('likes/',like_main_post, name='like_main_post'),
    path('comment/',comment, name='comment'),
    path('<int:pk>/update/',projectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/',projectDeleteView.as_view(), name='project-delete'),
    path('illegal/user/',illegal_tresspass,name='illegal-trespass'),
]