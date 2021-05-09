from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
import os

class quizcourse(models.Model):

    title = models.CharField(max_length=100,unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class quizLevels(models.Model):
    RATING_CHOICES = (
        ('Éasy', 'easy'),
        ('Medium', 'medium'),
        ('Hard', 'Hard'),
    )
    quizCourse_related = models.ForeignKey(quizcourse,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    level = models.CharField(max_length=100,choices=RATING_CHOICES)

    def __str__(self):
        return self.title
    
class question(models.Model):
    
    quiz = models.ForeignKey(quizLevels,on_delete=models.CASCADE)
    questions = models.CharField(max_length=100,unique=True)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.questions

# class answer(models.Model):

#     questionid = models.ForeignKey(question,on_delete=models.CASCADE)
#     ans = models.CharField(max_length=1000,unique=True)
#     is_correct = models.BooleanField(default=False)

#     def __str__(self):
#         return self.ans


