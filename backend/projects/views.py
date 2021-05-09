from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView
from django.http import HttpResponseRedirect, request,HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from event.models import *
from django.db.models import Count
try:
    from django.utils import simplejson as json
except ImportError:
    import json
# Create your views here.
class projectListView(LoginRequiredMixin,ListView):
    model = projects   
    template_name='projects-list.html'
    context_object_name='projects'
    ordering=['-date_posted']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = event.objects.all().annotate(num_tags=Count('userEnrolled')).order_by('-num_tags')[:4]
        context['comment_form'] = commentForm()
        context['events'] = events
        return context

class projectCreateView(LoginRequiredMixin,CreateView):
    model =  projects
    fields = ['video','description']
    template_name = 'project_createView.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def like_main_post(request):
    post = get_object_or_404(projects, id=request.POST.get('id',None))
    is_like = False
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        is_like = False
    else:
        is_like = True
        post.like.add(request.user)

    context = {
        'likes_count':post.like.count(),
        'is_like':is_like,
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


@login_required
def comment(request):
    print("jojo")
    prj = get_object_or_404(projects, id=request.POST.get('post_id',None))
    print(request.POST.get('id',None))
    if request.method == 'POST':
        comment = Comment(project=prj,user=request.user,body=request.POST.get('datas'))
        comment.save()

    context={
            'username': request.user.username,
            'userid':request.user.id,
            'body': request.POST.get('datas'),
            'image':request.user.profile.image.url,
            'date':str(comment.date_added),
            'number_of_comments': Comment.objects.filter(project=prj).all().count(),
        }

    return HttpResponse(json.dumps(context), content_type='application/json')




class projectDetailView(LoginRequiredMixin,DetailView):
    model = projects
    template_name = 'project_detail.html'
    def get_context_data(self, **kwargs):
        liked = True
        prj = get_object_or_404(projects,id=self.kwargs['pk'])
        total_like = prj.num_likes()

        if prj.like.filter(id=self.request.user.id).exists():
            liked = False
        
        context = super().get_context_data(**kwargs)
        context['total_like'] = total_like
        context['liked'] = liked
        return context

class projectUpdateView(LoginRequiredMixin,UpdateView):
    model = projects
    template_name  = 'project_edit.html'
    fields = ['video','description']

    # def get(self, request, *args, **kwargs):
    #     prj = self.get_object()
    #     if self.request.user == prj.user:
    #         return HttpResponseRedirect(reverse('illegal-trespass'))
    
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
        return False
    

class projectDeleteView(LoginRequiredMixin,DeleteView):
    model = projects
    template_name  = 'projects_confirm_delete.html'
    success_url = '/project/'

    def get(self, request, *args, **kwargs):
        prj = self.get_object()
        if self.request.user != prj.user:
            return HttpResponseRedirect(reverse('illegal-trespass'))
        else:
            return super().get(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

def illegal_tresspass(request):
    return render(request,'illegal.html')
