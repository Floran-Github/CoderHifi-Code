from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages


def event_dashboard(request):
    events = event.objects.filter(created_by=request.user)
    label = []
    data = []
    for i in events:
        label.append(i.title)
        data.append(i.userEnrolled.count())
    
    context = {
        'events' : events,
        'number_of_event' : events.count(),
        'label':label,
        'data':data,
    }
    return render(request,'dashboard.html',context=context)
    pass



class eventListView(ListView):
    model = event
    template_name = 'event-list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrolled_event'] = eventMaytoMany.objects.filter(userId=self.request.user)
        # context['comment_form'] = commentForm()
        return context

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

def enroll(request, pk):
    eventid = get_object_or_404(event,id=pk)
    userId = request.user
    enrollNo = f'{eventid.title} - {eventMaytoMany.objects.filter(eventId=eventid).count() + 1}'


    if eventid.userEnrolled.filter(id=request.user.id).exists():
        eventid.userEnrolled.remove(request.user)
    else:
        eventid.userEnrolled.add(request.user)
        eventManytoMany = eventMaytoMany(event_enroll_id = enrollNo,eventId = eventid,userId = userId)
        eventManytoMany.save()

    print("event enrolled")
    messages.add_message(request, messages.INFO, "enrolled in {eventid.title} successfully")
    return redirect('event-list')
    pass