from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.forms import widgets
from django.contrib.auth.models import User
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages
import datetime
from django.db.models import Q


def event_dashboard(request):
    events = event.objects.filter(created_by=request.user)
    label = []
    data = []
    for i in events:
        label.append(i.title)
        data.append(i.userEnrolled.count())
    
    context = {
        'events' : events[len(events)-2:],
        'number_of_event' : events.count(),
        'label':label,
        'data':data,
    }
    return render(request,'dashboard.html',context=context)
    pass

def event_list_dashboard(request):
    events = event.objects.filter(created_by=request.user)

    context = {
        'events':events,
    }

    return render(request,'event_list_dashboard.html',context=context)

def add_participant_event_list(request,pk):
    eventid = get_object_or_404(event,id=pk)
    evnt = eventMaytoMany.objects.filter(eventId=eventid)
    if 'term' in request.GET:
        user = User.objects.filter(username__icontains=request.GET.get('term'))
        user_name = list()
        for i in user:
            user_name.append(i.username)
        return JsonResponse(user_name, safe=False)


    context = {
        'object':eventid,
        'participant':evnt,
    }
    return render(request,'add_participant.html',context=context)

def add_participant(request,pk):
    
    if request.method == "POST":
        username = request.POST.get('search_name')
        user = User.objects.get(username=username)
        eventid = get_object_or_404(event,id=pk)
        enrollNo = f'{eventid.title} - {eventMaytoMany.objects.filter(eventId=eventid).count() + 1}'

        if eventid.userEnrolled.filter(id=user.id).exists():
            return redirect('event-add-participant',pk=pk)
        else:
            eventid.userEnrolled.add(user)
            eventManytoMany = eventMaytoMany(event_enroll_id = enrollNo,eventId = eventid,userId = user)
            eventManytoMany.save()
    return redirect('event-add-participant',pk=pk)


class eventListView(ListView):
    model = event
    template_name = 'event-list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['event_not_done'] = event.objects.filter(Q(last_day_of_registration=datetime.date.today()))

        event_enrolled = []
        a = eventMaytoMany.objects.filter(userId=self.request.user)
        b = event.objects.filter(Q(last_day_of_registration__gte=datetime.date.today()))

        for i in a:
            if i.eventId in b:
                event_enrolled.append(i)
        # context['comment_form'] = commentForm()
        context['enrolled_event'] = event_enrolled
        return context

class eventCreateView(CreateView):
    model = event
    fields = ['title','description','picture','cost','last_day_of_registration']
    template_name = 'event_create.html'

    def get_form(self):
        '''add date picker in forms'''
        form = super(eventCreateView, self).get_form()
        form.fields['last_day_of_registration'].widget = widgets.DateInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class eventUpdateView(LoginRequiredMixin,UpdateView):
    model = event
    template_name  = 'event_edit.html'
    fields = ['title','description','picture','cost','last_day_of_registration']

    def get_form(self):
        '''add date picker in forms'''
        form = super(eventUpdateView, self).get_form()
        form.fields['last_day_of_registration'].widget = widgets.DateInput(attrs={'type': 'date'})
        return form

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