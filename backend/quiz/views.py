from django.shortcuts import render,get_object_or_404
from .models import *
from .filters import *
from django.contrib.auth.models import User
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.core.paginator import Paginator
from django.http.response import HttpResponse
# Create your views here.

lst = []
answers = question.objects.all()
anslist = []
for i in answers:
    anslist.append(i.answer)
def index(request, pk):
    quizlevel = get_object_or_404(quizLevels,pk=pk)
    questions = question.objects.filter(quiz=quizlevel).all()
    count = questions.count()
    context = {
        'obj':questions,
        'count':count
           }
    return render(request,'quiz.html',context=context)
    # obj = question.objects.all()
    # count = question.objects.all().count()
    # paginator = Paginator(obj,1)
    # try:
    #    page = int(request.GET.get('page','1'))  
    # except:
    #     page =1
    # try:
    #     questions = paginator.page(page)
    # except(EmptyPage,InvalidPage):
        
    #     questions=paginator.page(paginator.num_pages)
            
    # return render(request,'quiz.html',{'obj':obj,'questions':questions,'count':count})
def result(request, pk):
    score =0
    for i in range(len(lst)):
        if lst[i]==anslist[i]:
            score +=1
    return render(request,'result.html',{'score':score,'lst':lst})
def save_ans(request, pk):
    ans = request.GET['ans']
    lst.append(ans)
def welcome(request, pk):
    lst.clear()
    return render(request,'quiz_level.html')

def getanswer(request):
    if request.method=='POST':
        answer=request.POST.getlist('ans[]')
        print(answer)

        return HttpResponse('{"status":"success", "msg":"success"}', content_type='application/json')

    
# def quiz(request):
#     quizes=quizcourse.objects.filter(created_by=request.user)
#     # number_of_quiz_enrolled = 0
#     title = []
#     desciption = []

#     for i in quizes:
#         title.append(i.title)
#         desciption.append(i.description)
#         # number_of_quiz_enrolled += i.studentEnrolled.count()

#     context = {
#         # 'name_of_quize': quizes.count(),
#         'title': title,
#         'desciption': desciption,
#     }

#     return render (request, 'courses.html',context=context)


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
        context['object'] = quizLevels.objects.filter(quizCourse_related=self.object)
        return context


# class ActualQuiz(LoginRequiredMixin,DetailView):
    # model = quizLevels
    # template_name = 'quiz.html'
    # context_object_name = 'object'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['question'] = question.objects.filter(quiz=self.object).all()


        # return context

