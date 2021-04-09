from django.shortcuts import render
from .models import *
from .filters import *
from django.contrib.auth.models import User
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin

# Create your views here.

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


class ActualQuiz(LoginRequiredMixin,DetailView):
    model = quizLevels
    template_name = 'quiz.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = question.objects.filter(quiz=self.object).all()


        return context

