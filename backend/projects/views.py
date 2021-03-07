from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.urls import reverse
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView
from django.http import HttpResponseRedirect, request,HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
# Create your views here.
class projectListView(LoginRequiredMixin,ListView):
    model = projects   
    template_name='projects-list.html'
    context_object_name='projects'
    ordering=['-date_posted']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = commentForm()
        return context

class projectCreateView(LoginRequiredMixin,CreateView):
    model =  projects
    fields = ['video','description']
    template_name = 'project_createView.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def like_main_post(request, pk):
    post = get_object_or_404(projects, id=request.POST.get('post_id'))

# unlike and like condition
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
    
    return HttpResponseRedirect(reverse('project-list')) 

@login_required
def comment(request):
    prj = get_object_or_404(projects,id=request.POST.get('comment_id'))
    if request.method == 'POST':
        form = commentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = Comment(project=prj,user=request.user,body=form.cleaned_data['body'])
            comment.save()

    return redirect('project-list')



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
