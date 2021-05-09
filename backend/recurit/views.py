from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User,Group
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages
import datetime
from users.models import *
from django.db.models import Count, Q

class jobList(LoginRequiredMixin,ListView):
    model = jobPost
    template_name = 'job-list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['event_not_done'] = event.objects.filter(Q(last_day_of_registration=datetime.date.today()))
        a = jobPost.objects.all()
        is_company = 0
        userp = get_object_or_404(Profile,user=self.request.user)
        user = get_object_or_404(User,id=self.request.user.id)

        b = []
        if user.groups.filter(name='recruiter'):
            finalList = a
            is_company = 1
            pass
        else:
            for i in userp.languages_prefer.all():
                for j in jobPost.objects.filter(skills=i).all().order_by('-id'):
                    b.append(j)
            finalList = set(b)

            pass
        context['jobs'] = finalList
        context['is_company'] = is_company
        return context


class allJob(LoginRequiredMixin,ListView):
    model = jobPost
    template_name = 'explore_jobs.html'

    def get_context_data(self,**kwargs):
        context =  super().get_context_data(**kwargs)
        context['jobs'] = jobPost.objects.all().order_by('-id')
        context['tops'] = jobPost.objects.all().annotate(num_tags=Count('applied_people')).order_by('-num_tags')[:2]

        return context

################################################
###### dashboard
class jobCreate(LoginRequiredMixin,CreateView):
    model = jobPost
    template_name = 'job-create.html'
    fields = ['job_title','job_description','roles_And_responsibilities','skills','no_of_position','seniority_level','employment_type','deadline','salary']
    def get_form(self):
        '''add date picker in forms'''
        form = super(jobCreate, self).get_form()
        form.fields['deadline'].widget = widgets.DateInput(attrs={'type': 'date'})
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        return form

    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)

class jobUpdate(LoginRequiredMixin,UpdateView):
    model = jobPost
    template_name = 'job-update.html'
    fields = ['job_title','job_description','roles_And_responsibilities','skills','no_of_position','seniority_level','employment_type','deadline','salary']
    
    def get_form(self):
        '''add date picker in forms'''
        form = super(jobUpdate, self).get_form()
        form.fields['deadline'].widget = widgets.DateInput(attrs={'type': 'date'})
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        return form
    
    def get(self, request, *args, **kwargs):
        event = self.get_object()
        if self.request.user != event.company:
            return HttpResponseRedirect(reverse('illegal-trespass'))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)


    def test_func(self):
        event = self.get_object()
        if self.request.user == event.company:
            return True
        return False


class jobDetail(LoginRequiredMixin,DetailView):
    model = jobPost
    template_name = 'job-detail.html'

def apply(request,pk):
    jobid = get_object_or_404(jobPost,id=pk)
    if jobid.applied_people.filter(id=request.user.id).exists():
        jobid.applied_people.remove(request.user)
    else:
        jobid.applied_people.add(request.user)

    return redirect('job-detail',pk=pk)


def dash(request):
    user = get_object_or_404(User,id=request.user.id)
    if user.groups.filter(name='recruiter'):
        a = jobPost.objects.filter(company=request.user)
        label = []
        data = []
        for i in a:
            label.append(i.job_title)
            data.append(i.applied_people.count())

        context = {
            'number':a.count(),
            'label':label,
            'data':data,
        }

        return render(request,'jdashboard.html',context)
    else:
        return redirect('illegal-trespass')
    pass

class jobdashlist(LoginRequiredMixin,ListView):
    model = jobPost
    template_name = 'job-dash-list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['event_not_done'] = event.objects.filter(Q(last_day_of_registration=datetime.date.today()))
        a = jobPost.objects.filter(company=self.request.user)
        context['jobs'] = a
        return context

class viewpeople(LoginRequiredMixin,DetailView):
    model = jobPost
    template_name = 'view-people.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        print(self.object.applied_people.all().count())
        skill = []
        verified = []
        unverified = []
        applies = self.object.applied_people.all()
        for i in self.object.skills.all():
            skill.append(i)
        
        for i in applies:
            count = 0
            for j in i.profile.languages_prefer.all():
                if j in skill:
                    count = 1
                    verified.append(i)
                    break
            if count != 1:
                unverified.append(i)               

        context['verified'] = verified
        context['unverified'] = unverified
        return context



    