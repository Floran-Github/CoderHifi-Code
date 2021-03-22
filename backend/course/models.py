from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
# Create your models here


def video_validator(value):
    limit = 2 * 1024 * 1024
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4','.mov','.wmv','.avi','.mkv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    # if value.size > limit:
    #     raise ValidationError('File too large. Size should not exceed 2 MiB.')
    #  validators=[video_validator],
    pass

class Type_category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class language_category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class course(models.Model):
    teacherId = models.ForeignKey(User,on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200,unique=True)
    fees = models.IntegerField(default=0)
    studentEnrolled = models.ManyToManyField(User,related_name="enrolled_student", blank=True, default=None)
    
class module(models.Model):
    course_associate = models.ForeignKey(course,on_delete=models.CASCADE)
    module_name = models.CharField("Name",max_length=100)
    Description = models.TextField()
    
    def __str__(self):
        return f'{self.module_name} of {str(self.course.course_name)}'

class videoContent(models.Model):
    module_associated = models.ForeignKey(module,on_delete=models.CASCADE)
    video = models.FileField(upload_to="course_content" ,validators=[video_validator])
    description = models.TextField()

    def __str__(self):
        return f'{str(self.module_associated.module_name)} - module'

class DescriptionContent(models.Model):
    moduke_associated = models.ForeignKey(module,on_delete=models.CASCADE)
    description = models.TextField()
     
    def __str__(self):
        return f'{str(self.module_associated.module_name)} - module'

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    course = models.ForeignKey(course, related_name='reviews')
    pub_date = models.DateTimeField(auto_now_add=True)
    user_name = models.ForeignKey(User, related_name='reviewers')
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)