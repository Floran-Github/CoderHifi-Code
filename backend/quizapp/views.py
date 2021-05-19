from django.shortcuts import render,get_object_or_404
from .models import *
from .filters import *
from django.contrib.auth.models import User
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.core.paginator import Paginator
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import *
try:
    from django.utils import simplejson as json
except ImportError:
    import json
# Create your views here.


def index(request, pk):
    quizlevel = get_object_or_404(quizLevels,pk=pk)
    question = questions.objects.filter(quiz=quizlevel).all()
    count = question.count()
    context = {
        'quizlevel':pk,
        'obj':question,
        'count':count
           }
    return render(request,'quiz.html',context=context)



def createPage(request):
    a = 9
    quiz =  quizLevels.objects.filter(quizCourse_related=request.session.get('gxgrff')).all()
    return render(request,'createquiz.html',{'id':request.session.get('gxgrff'),'quiz':quiz})

@csrf_exempt
def createquiz(request):
    status = "fail"
    if request.method == 'POST':
        question = request.POST.getlist('questions[]')
        correctans = request.POST.getlist('correctans[]')
        answers = request.POST.getlist('answer[]')
        mark = request.POST.getlist('marks[]')
        quiz =  get_object_or_404(quizLevels,pk=request.POST.get('module'))
        print(request.session.get('gxgrff'))
        print(question)
        print(correctans)
        print(answers)
        print(request.POST.get('module'))

        for i in range(0,len(question)):
            j = 0
            print(question[i])
            print(answers[i+j+0])
            print(answers[i+j+1])
            print(answers[i+j+2])
            print(answers[i+j+3])
            print('correct ',answers[i])
            ques = questions(quiz=quiz,questions=question[i],option1=answers[i+j+0],option2=answers[i+j+1],option3=answers[i+j+2],option4=answers[i+j+3],answer=answers[i],marks=mark[i])
            ques.save()
            status = "success"
            j += 3
            

        context = {
            'status':status
        }

        return HttpResponse(json.dumps(context), content_type='application/json')
    pass

@csrf_exempt
def getanswer(request):
    if request.method=='POST':
        print('in fucntion')
        print(request.POST.get('quizlevel'))
        quizlevel = get_object_or_404(quizLevels,pk=request.POST.get('quizlevel'))
        question = questions.objects.filter(quiz=quizlevel).all()
        answer=request.POST.getlist('ans[]')
        marks = 0
        total = 0
        status = 'Fail'
        result = []
        for i in range(len(question)):
            total += question[i].marks
            if question[i].answer == answer[i]:
                marks += question[i].marks
                result.append(1)
            else:
                result.append(0)

        if userParticipated.objects.filter(user=request.user,quiz=quizlevel):
            userQuizData = userParticipated.objects.get(user=request.user,quiz=quizlevel)
            userQuizData.score = marks
            userQuizData.save(update_fields=['score'])
        else:
            userQuizData = userParticipated(user=request.user,quiz=quizlevel,score=marks)
            userQuizData.save()

        if total * 0.6 <= marks:
            status = 'Pass'
            if not quizlevel.peoplePassed.filter(id=request.user.id).exists():
                quizlevel.peoplePassed.add(request.user)
            


        print(request.POST.get('quizlevel'))
        print(answer)
        context = {
            'mark':marks,
            'totalmark':total,
            'result': result,
            'teststatus':status,
            'status':"success"
        }

        return HttpResponse(json.dumps(context), content_type='application/json')

  

class MainQuizList(LoginRequiredMixin,ListView):
    model = quizcourse
    template_name = "courses.html"
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = quizFilter(self.request.GET,queryset = self.get_queryset())

        return context

class quizLevel(LoginRequiredMixin,DetailView):
    model = quizcourse
    template_name = 'quiz_level.html'
    context_object_name = 'quiz_info'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['gxgrff'] = self.object.pk
        context['object'] = quizLevels.objects.filter(quizCourse_related=self.object)
        context['status'] = self.check
        return context

    def automatically_save(self,request):
        data = quizLevels.objects.filter(quizCourse_related=self.kwargs['pk'])
        self.check = False
        for i in data:
            self.check = False
            if i.peoplePassed.filter(id=request.user.id).exists():
                self.check = True
            
        print(self.check)
        if self.check == True:
            quizData = quizcourse.objects.get(id=self.kwargs['pk'])
            profile = Profile.objects.get(user=request.user)
            
            if not quizData.peoplePassed.filter(id = request.user.id).exists():
                profile.rating += 10
                profile.save(update_fields=['rating'])
                quizData.peoplePassed.add(request.user)

            pass

    def dispatch(self, request, *args, **kwargs):
        print(self.kwargs['pk'])
        self.automatically_save(request)
        return super(quizLevel, self).dispatch(request, *args, **kwargs)


