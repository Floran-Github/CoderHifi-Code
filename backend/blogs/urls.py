from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',blogListView.as_view(),name='blog-list'),
    path('create/',blogCreateView.as_view(),name='blog-create'),
    path('likes/<int:pk>',like_main_post, name='like_main_post'),
    path('comment/',comment, name='comments'),
    path('<int:pk>/update/',blogUpdateView.as_view(), name='blog-update'),
    path('<int:pk>/delete/',blogDeleteView.as_view(), name='blog-delete'),
    path('illegal/user/',illegal_tresspass,name='blog-illegal-trespass'),
]