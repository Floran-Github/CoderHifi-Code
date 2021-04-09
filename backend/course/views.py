from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.forms import widgets
from django.contrib.auth.models import User
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages
import datetime
from django.db.models import Q,Count
from django.contrib.auth.decorators import login_required
from users.models import *

def teacher_dashboard(request):
    teacher_course = course.objects.filter(teacherId = request.user)
    number_of_student_enrolled = 0
    label = []
    data = []

    for i in teacher_course:
        label.append(i.course_name)
        data.append(i.studentEnrolled.count())
        number_of_student_enrolled += i.studentEnrolled.count()
    

    context = {
        'number_of_course' : teacher_course.count(),
        'number_of_student' : number_of_student_enrolled,
        'recent_course' : teacher_course[len(teacher_course):],
        'label':label,
        'data':data,
    }

    return render(request,'course-dashboard.html',context=context)

class dashboardCourseListView(LoginRequiredMixin,ListView):
    model = course
    template_name = "course-list-dashboard.html"
    context_object_name = 'dashboard-course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_course'] = course.objects.filter(teacherId=self.request.user)

        return context

class dashboardCourseDetailView(LoginRequiredMixin,DetailView):
    model = course
    template_name = "course-module-list-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['dxdrp'] = self.object.pk
        context['module'] = module.objects.filter(course_associate=self.object)
        return context

class dashboardModuleDetailView(LoginRequiredMixin,DetailView):
    model = module
    template_name = "course-content-list-dashboard.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        self.request.session['dxdrf'] = self.object.pk
        context['content'] = Content.objects.filter(module_associated=self.object)
        return context

class courseListView(LoginRequiredMixin,ListView):
    model = course
    template_name='course-list.html'
    context_object_name='courses'


class MaincourseListView(LoginRequiredMixin,ListView):
    model = course
    template_name='main-course-list.html'
    context_object_name='course'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        event_enrolled = []
        trend_course = []
        a = course.objects.all()
        for i in a:
            if i.studentEnrolled.filter(id=self.request.user.id).exists():
                event_enrolled.append(i)
        trend = course.objects.annotate(q_count=Count('studentEnrolled')).order_by('-q_count')[:3]
        for i in trend:
            if i.studentEnrolled.filter(id=self.request.user.id).exists():
                pass
            else:
                trend_course.append(i)
        context['enrolled_course'] = event_enrolled
        context['trend'] = trend_course
        context['length'] = len(event_enrolled)
        return context
        
class courseCreateView(LoginRequiredMixin,CreateView):
    model = course
    template_name = 'course-create-dashboard.html'
    fields = ['course_name','thumbnail_image','course_description','course_type','language_type','fees']

    def form_valid(self, form):
        form.instance.teacherId = self.request.user
        return super().form_valid(form)

class moduleCreateView(LoginRequiredMixin,CreateView):
    model = module
    template_name = 'course-module-create-dashboard.html'
    fields = ['module_name','module_image','Description']


    def form_valid(self, form):
        course_pk = self.request.session.get('dxdrp')
        course_foreign =get_object_or_404(course,pk=course_pk)
        self.object = form.save(commit=False)
        self.object.course_associate = course_foreign
        self.object.save()
        return super().form_valid(form)
class contentCreateView(LoginRequiredMixin,CreateView):
    model = Content
    template_name = 'course-content-create-dashboard.html'
    fields = ['content_name','video','description','is_description_content']

    def form_valid(self, form):
        module_pk = self.request.session.get('dxdrf')
        module_foreign =get_object_or_404(module,pk=module_pk)
        self.object = form.save(commit=False)
        self.object.module_associated = module_foreign
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('course-dashboard-module-detail',kwargs={'pk':self.request.session.get('dxdrf')})
class courseDetailView(DetailView):
    model = course
    template_name = 'course_detail.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        review_list = []
        reviews = Review.objects.filter(course=self.object)

        for i in reviews:
            review_list.append(i.rating)
        if len(review_list) == 0:
            rating = 0
        else:
            rating = sum(review_list)/len(review_list)
        self.request.session['dxdrf'] = self.object.pk
        context['review'] = Review.objects.filter(course=self.object)
        context['rating'] = rating

        return context
    
class courseUpdate(LoginRequiredMixin,UpdateView):
    model = course
    fields = ['course_name','thumbnail_image','course_description','course_type','language_type','fees']
    template_name = 'course-update.html'

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        if self.request.user != event.teacherId:
            return HttpResponseRedirect(reverse('illegal-trespass'))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.teacherId = self.request.user
        return super().form_valid(form)

class modeleUpdate(LoginRequiredMixin,UpdateView):
    model = module
    template_name = 'module-update.html'
    fields = ['module_name','module_image','Description']

class contentUpdate(LoginRequiredMixin,UpdateView):
    model = Content
    template_name = 'content-update.html'
    fields = ['content_name','video','description','is_description_content']


    def get_success_url(self):
        return reverse('course-dashboard-module-detail',kwargs={'pk':self.request.session.get('dxdrf')})


##########################################
###################### ENROLLEMENT #######
##########################################

class enrollCourse(LoginRequiredMixin,DetailView):
    model = course
    template_name = 'enrolled_course_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = module.objects.filter(course_associate=self.object)
        b = 1
        for i in a:
            if i.studentCompleted.filter(id=self.request.user.id).exists():
                pass
            else:
                b =0 
        context['module'] = module.objects.filter(course_associate=self.object)
        context['completed'] = b
        return context


def Enroll(request,pk):
    courseId = get_object_or_404(course,id=pk)


    if courseId.studentEnrolled.filter(id=request.user.id).exists():
        return redirect('enroll-course',pk=int(pk))
    else:
        courseId.studentEnrolled.add(request.user)
    
    return redirect('enroll-course',pk=int(pk))


class enrollModule(LoginRequiredMixin,DetailView):
    model = module
    template_name = 'enroll_module.html'
    

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        self.request.session['dxdrff'] = self.object.pk
        a = Content.objects.filter(module_associated=self.object)
        b = 1
        for i in a:
            if i.studentCompleted.filter(id=self.request.user.id).exists():
                pass
            else:
                b =0
        
        context['module'] = Content.objects.filter(module_associated=self.object)
        context['completed'] = b
        return context

class content(LoginRequiredMixin,DetailView):
    model = Content
    template_name = 'content.html'

#######################################
########### complete ##################
#######################################

def completeContent(request,pk):
    contentId = get_object_or_404(Content,id=pk)
    if contentId.studentCompleted.filter(id=request.user.id).exists():
        pass
    else:
        contentId.studentCompleted.add(request.user)
    
    return  redirect('enroll-module',pk=int(contentId.module_associated.id))


def completedModule(request,pk):
    moduleId  = get_object_or_404(module,id=pk)
    print(moduleId)
    if moduleId.studentCompleted.filter(id=request.user.id).exists():
        pass
    else:
        moduleId.studentCompleted.add(request.user)
    
    return  redirect('enroll-course',pk=int(moduleId.course_associate.id))

def completedCourse(request,pk):
    courseid  = get_object_or_404(course,id=pk)
    print(courseid)
    if courseid.studentCompleted.filter(id=request.user.id).exists():
        pass
    else:
        courseid.studentCompleted.add(request.user)
        profile = Profile.objects.get(user=request.user)

        for i in courseid.language_type.all():
            if profile.languages_prefer.filter(id=i.id).exists():
                pass
            else:
                profile.languages_prefer.add(i)

    return  redirect('enroll-course',pk=int(courseid.id))


###################################
#### discussion panel #############
###################################


class discussionListView(LoginRequiredMixin,ListView):
    model = discussionpanel   
    template_name='discussionpanel-list.html'
    context_object_name='blogs'
    ordering=['-date_posted']

   

class blogCreateView(LoginRequiredMixin,CreateView):
    model =  discussionpanel
    fields = ['title','description']
    template_name = 'discuss-create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class blogtDetailView(LoginRequiredMixin,DetailView):
    model = discussionpanel
    template_name = 'discuss-detail.html'
    context_object_name='blog'

    def get_context_data(self, **kwargs):
        liked = True
        prj = get_object_or_404(discussionpanel,id=self.kwargs['pk'])
        total_like = prj.num_likes()

        if prj.bloglike.filter(id=self.request.user.id).exists():
            liked = False
        
        context = super().get_context_data(**kwargs)
        context['total_like'] = total_like
        context['liked'] = liked
        context['comment_form'] = commentForm()
        return context

class blogUpdateView(LoginRequiredMixin,UpdateView):
    model = discussionpanel
    template_name  = 'discuss-create.html'
    fields = ['title','description']

    def get(self, request, *args, **kwargs):
        prj = self.get_object()
        if self.request.user != prj.user:
            return HttpResponseRedirect(reverse('illegal-trespass'))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def test_func(self):
        prj = self.get_object()
        if self.request.user == prj.user:
            return True
        return HttpResponseRedirect(reverse('blog-illegal-trespass'))
    

class blogDeleteView(LoginRequiredMixin,DeleteView):
    model = discussionpanel
    template_name  = 'blogs_confirm_delete.html'
    success_url = '/blog/'

    def get(self, request, *args, **kwargs):
        prj = self.get_object()
        if self.request.user != prj.user:
            return HttpResponseRedirect(reverse('blog-illegal-trespass'))
        else:
            return super().get(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


@login_required
def like_main_post(request, pk):
    post = get_object_or_404(discussionpanel, id=request.POST.get('post_id'))

# unlike and like condition
    if post.bloglike.filter(id=request.user.id).exists():
        post.bloglike.remove(request.user)
    else:
        post.bloglike.add(request.user)
    
    return redirect('discuss-det',pk=post.id)

@login_required
def comment(request):
    prj = get_object_or_404(discussionpanel,id=request.POST.get('comment_id'))
    if request.method == 'POST':
        form = commentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = discussionComment(blog=prj,user=request.user,body=form.cleaned_data['body'])
            comment.save()

    return redirect('discuss-det',pk=prj.id)