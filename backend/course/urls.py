from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',MaincourseListView.as_view(),name='main-course-list'),
    path('explore/',courseListView.as_view(),name='course-list'),
    path('create/',courseCreateView.as_view(),name='course-create'),
    # path('',courseListView.as_view(),name='course-list'),
    path('dashboard/',teacher_dashboard,name='course-dashboard'),
    path('dashboard/list',dashboardCourseListView.as_view(),name='course-dashboard-list'),

    path('dashboard/course/create',courseCreateView.as_view(),name='course-dashboard-create'),
    path('dashboard/course/module/create',moduleCreateView.as_view(),name='course-dashboard-module-create'),
    path('dashboard/course/module/content/create',contentCreateView.as_view(),name='course-dashboard-content-create'),
    
    path('dashboard/course/<int:pk>',dashboardCourseDetailView.as_view(),name='course-dashboard-detail'),
    path('dashboard/course/module/<int:pk>',dashboardModuleDetailView.as_view(),name='course-dashboard-module-detail'),
    path('detail/<int:pk>/',courseDetailView.as_view(),name='course-detail'),
    
    path('dashboard/course/update/<int:pk>',courseUpdate.as_view(),name='course-dashboard-update'),
    path('dashboard/course/module/update/<int:pk>',modeleUpdate.as_view(),name='module-dashboard-update'),
    path('dashboard/course/module/content/update/<int:pk>',contentUpdate.as_view(),name='content-dashboard-update'),

    path('course/<int:pk>/',enrollCourse.as_view(),name='enroll-course'),
    path('course/module/<int:pk>/',enrollModule.as_view(),name='enroll-module'),
    path('course/module/content/<int:pk>/',content.as_view(),name='enroll-content'),
    path('course/enroll/<int:pk>/',Enroll,name='enroll'),

    path('course/module/content/completed/<int:pk>/',completeContent,name='completed-content'),
    path('course/module/completed/<int:pk>/',completedModule,name='completed-module'),
    path('course/completed/<int:pk>/',completedCourse,name='completed-course'),
    path('course/review/',review.as_view(),name='review'),
    
    path('course/discussoin/',discussionListView.as_view(),name='discuss'),
    path('course/discussoin/create',discussionCreateView.as_view(),name='discuss-create'),
    path('course/discussoin/<int:pk>',discussionDetailView.as_view(),name='discuss-det'),
    path('course/likes/<int:pk>',like_main_post, name='di-like_main_post'),
    path('course/comment/',comment, name='di-comments'),

    path('search/',search,name="search"),

    
]