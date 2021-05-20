from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,TeacherProfile,CompanyProfile
from django.contrib.auth.models import Group, User
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.db.models import Q
import datetime
from .models import *
from course.models import *
from quizapp.models import *
from recurit.models import *
import datetime
# Create your views here.

def rec_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profileform = CompanyProfile(request.POST)
        
        if form.is_valid():
            user = form.save()  
            profile = profileform.save(commit=False)
            profile.user = user
            profile.save()
            group = Group.objects.get(name='recruiter')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} !')
            return redirect('login')


    else:
        form = UserRegisterForm()
        profileform = CompanyProfile()

    context = {
        'form':form,
        'p_form':profileform,
        'status':'create'
    }


    return render(request, 'users/comp-register.html', context=context)

def company_profile_update(request):
    print('update')
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,instance=request.user)
        profileform = CompanyProfile(request.POST,request.FILES,instance=request.user.recruiter_profile)
        
        if form.is_valid():
            user = form.save()  
            profile = profileform.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account updated for {username} !')
            return redirect('company-profile',username=request.user.username)
        else:
            print('error')
            messages.error(request,'Error occurred')
            return redirect('company-update')


    else:
        form = UserUpdateForm(instance=request.user)
        profileform = CompanyProfile(instance=request.user.recruiter_profile)
    context = {
        'form':form,
        'p_form':profileform,
        'status':'update'
    }

    return render(request, 'users/comp-register.html', context=context)

def update_teacher_profile(request):
    if request.method == 'POST':
        form = TeacherProfile(request.POST,request.FILES,instance=request.user.teacher_profile)
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, f'Teaher Profile updated ')
            return redirect('teacher-profile',username=request.user.username)
        else:
            print('error')
            messages.error(request,'Error occurred')
            return redirect('company-update')


    else:
        form = TeacherProfile(instance=request.user.teacher_profile)
    context = {
        'form':form,
        'status':'update'
    }

    return render(request, 'users/teacher_register.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()   #this will save the content in database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} !')
            return redirect('login')


    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form' : form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    courses = course.objects.all()
    quizs = quizcourse.objects.all()
    completed_course = []
    enrolled_course = []
    quiz_completed = []
    for i in courses:
        if i.studentEnrolled.filter(id=request.user.id).exists():
            if i.studentCompleted.filter(id=request.user.id).exists():
                completed_course.append(i)
            else:
                enrolled_course.append(i)
    for i in quizs:
        if i.peoplePassed.filter(id=request.user.id).exists():
            quiz_completed.append(i)


    context = {
        'u_form':u_form,
        'p_form':p_form,
        'completed':completed_course,
        'enrolled':enrolled_course,
        'quizs':quiz_completed,
    }
    return render(request, 'users/profile.html',context)

def view_job_profile(request,username):
    user = get_object_or_404(User,username=username)
    recruiter = recruiter_profile.objects.filter(user=user)
    jobs = jobPost.objects.filter(Q(deadline=datetime.date.today()),company=user).all()
    context = {
        'object':recruiter[0],
        'jobs':jobs
    }
    return render(request,'users/job_profile.html',context=context)


def view_teacher(request,username):
    user = get_object_or_404(User,username=username)
    teacher = teacher_profile.objects.filter(user=user)
    courses = course.objects.filter(teacherId=user).all()
    print(teacher)
    context = {
        'object':user,
        'teacher':teacher[0],
        'courses':courses
    }

    return render(request,'users/teacher_profile.html',context=context)
    
    pass

def update_to_teacher(request):
    if request.user.is_staff == False:
        if request.method == "POST":
            form = TeacherProfile(request.POST)
            if form.is_valid():

                form_1 = form.save(commit=False)
                form_1.user = request.user
                form_1.save()
                user = User.objects.get(id=request.user.id)
                user.is_staff =True
                user.save()
                
                return redirect('course-dashboard')
        else:
            form = TeacherProfile()

        return render(request, 'users/teacher_register.html', {'form' : form,'status':'create'})     
    else:
        return render(request,'users/congratulation.html')


class shareProfile(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'users/share_profile.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = course.objects.all()
        quizs = quizcourse.objects.all()
        completed_course = []
        enrolled_course = []
        quiz_completed = []

        for i in courses:
            if i.studentEnrolled.filter(id=self.object.id).exists():
                if i.studentCompleted.filter(id=self.object.id).exists():
                    completed_course.append(i)
                else:
                    enrolled_course.append(i)

        for i in quizs:
            if i.peoplePassed.filter(id=self.object.id).exists():
                quiz_completed.append(i)

        context['enrolled'] = enrolled_course
        context['completed'] = completed_course
        context['quizs'] = quiz_completed
        return context



