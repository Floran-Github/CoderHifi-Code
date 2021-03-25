from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.forms import widgets
from django.contrib.auth.models import User
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages
import datetime
from django.db.models import Q


def teacher_dashboard(request):
    teacher_course = course.objects.filter(teacherId = request.user)
    label = []
    data = []

    for i in teacher_course:
        label.append(i.course_name)
        data.append(i.studentEnrolled.count())
    pass



class courseListView(LoginRequiredMixin,ListView):
    model = course
    template_name='course-list.html'
    context_object_name='courses'


class courseCreateView(LoginRequiredMixin,CreateView):
    model = course
    template_name = 'course-create.html'
    fields = ['course_name','thumbnail_image','course_description','course_type','language_type','fees']

    def form_valid(self, form):
        form.instance.teacherId = self.request.user
        return super().form_valid(form)

class courseDetailView(DetailView):
    model = course
    template_name = 'course_detail.html'
    
