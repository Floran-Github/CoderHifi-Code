from django.db import models

# Create your models here.
from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
import os

class quizcourse(models.Model):

    title = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    peoplePassed = models.ManyToManyField(User,blank=True,null=True)

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
    peoplePassed = models.ManyToManyField(User,blank=True,null=True)
    def __str__(self):
        return self.title
    
class questions(models.Model):
    
    quiz = models.ForeignKey(quizLevels,on_delete=models.CASCADE)
    questions = models.CharField(max_length=100,unique=True)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    marks = models.IntegerField()

    def __str__(self):
        return self.questions

class userParticipated(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quiz = models.ForeignKey(quizLevels,on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.user} marks on {self.quiz} : {self.score}'

