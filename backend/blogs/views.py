from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.urls import reverse
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView
from django.http import HttpResponseRedirect, request,HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin

# Create your views here.

class blogListView(LoginRequiredMixin,ListView):
    model = blogs   
    template_name='blogs-list.html'
    context_object_name='blogs'
    ordering=['-date_posted']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = commentForm()
        return context

class blogCreateView(LoginRequiredMixin,CreateView):
    model =  blogs
    fields = ['image','video','description']
    template_name = 'blog_createView.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def like_main_post(request, pk):
    post = get_object_or_404(blogs, id=request.POST.get('post_id'))

# unlike and like condition
    if post.bloglike.filter(id=request.user.id).exists():
        post.bloglike.remove(request.user)
    else:
        post.bloglike.add(request.user)
    
    return HttpResponseRedirect(reverse('blog-list')) 

@login_required
def comment(request):
    prj = get_object_or_404(blogs,id=request.POST.get('comment_id'))
    if request.method == 'POST':
        form = commentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = blogComment(blog=prj,user=request.user,body=form.cleaned_data['body'])
            comment.save()

    return redirect('blog-list')



class blogtDetailView(LoginRequiredMixin,DetailView):
    model = blogs
    template_name = 'blog_detail.html'
    def get_context_data(self, **kwargs):
        liked = True
        prj = get_object_or_404(blogs,id=self.kwargs['pk'])
        total_like = prj.num_likes()

        if prj.like.filter(id=self.request.user.id).exists():
            liked = False
        
        context = super().get_context_data(**kwargs)
        context['total_like'] = total_like
        context['liked'] = liked
        return context

class blogUpdateView(LoginRequiredMixin,UpdateView):
    model = blogs
    template_name  = 'blog_edit.html'
    fields = ['image','video','description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def test_func(self):
        prj = self.get_object()
        if self.request.user == prj.user:
            return True
        return HttpResponseRedirect(reverse('illegal-trespass'))
    

class blogDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = blogs
    template_name  = 'blogs_confirm_delete.html'
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

def illegal_tresspass(request):
    return render(request,'illegal.html')
