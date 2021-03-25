from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,TeacherProfile
from django.contrib.auth.models import User
from .models import *
# Create your views here.
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
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profile.html',context)

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
                print(user)
        else:
            form = TeacherProfile()

        return render(request, 'users/teacher_register.html', {'form' : form})     
    else:
        pass



def share_profile(request,username):
    pass