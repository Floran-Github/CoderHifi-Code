from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
import os 
# Create your models here.
class Type_category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class language_category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class jobPost(models.Model):
    company = models.ForeignKey(User,on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    roles_And_responsibilities = models.TextField()
    skills = models.ManyToManyField(language_category,default=None)
    no_of_position = models.IntegerField()
    deadline = models.DateField(default=timezone.now)
    posted_on = models.DateField(auto_now=True)
    seniority_level = models.CharField(max_length=50)
    employment_type = models.CharField(max_length=50)
    salary =models.IntegerField(null=True,blank=True)
    applied_people = models.ManyToManyField(User,related_name='applied_people',blank=True, default=None)
    def __str__(self):
        return self.job_title

    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk': self.pk})
    
