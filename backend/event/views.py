from django.shortcuts import render
from .models import *
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
# Create your views here.


class eventListView(ListView):
    model = event
    template_name = 'event-list.html'
    context_object_name = 'events'
    

class eventCreateView(CreateView):
    model = event
    fields = ['title','description','picture','cost','last_day_of_registration']
    template_name = 'event_create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class eventUpdateView(LoginRequiredMixin,UpdateView):
    model = event
    template_name  = 'event_edit.html'
    fields = ['title','description','picture','cost','last_day_of_registration']

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        if self.request.user != event.created_by:
            return HttpResponseRedirect(reverse('illegal-trespass'))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.created_by:
            return True
        return False


class eventDeleteView(LoginRequiredMixin,DeleteView):
    model = event
    template_name  = 'event_confirm_delete.html'
    success_url = '/event/'

    def get(self, request, *args, **kwargs):
        prj = self.get_object()
        if self.request.user != prj.created_by:
            return HttpResponseRedirect(reverse('illegal-trespass'))
        else:
            return super().get(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created_by:
            return True
        return False