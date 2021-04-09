from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
from django.urls import reverse
from django.utils import timezone
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
    thumbnail_image = models.ImageField(upload_to="course_thubnail",default='course_default.jpg')
    course_name = models.CharField(max_length=200,unique=True)
    course_description = models.TextField()
    course_type = models.ForeignKey(Type_category,on_delete=models.CASCADE)
    language_type = models.ForeignKey(language_category,on_delete=models.CASCADE)
    fees = models.IntegerField(default=0)
    studentEnrolled = models.ManyToManyField(User,related_name="enrolled_student", blank=True, default=None)
    studentCompleted = models.ManyToManyField(User,related_name="completed_student", blank=True, default=None)
    
    def __str__(self):
        return self.course_name

    def get_absolute_url(self):
        return reverse('course-dashboard-detail', kwargs={'pk': self.pk})
class module(models.Model):
    course_associate = models.ForeignKey(course,on_delete=models.CASCADE,related_name="module")
    module_image = models.ImageField(upload_to="course_thubnail",default='course_default.jpg')
    module_name = models.CharField("Name",max_length=100)
    Description = models.TextField()
    studentCompleted = models.ManyToManyField(User,related_name="completed_student_module", blank=True, default=None)
    
    def __str__(self):
        return f'{self.module_name} of {str(self.course_associate.course_name)}'

    def get_absolute_url(self):
        return reverse('course-dashboard-module-detail', kwargs={'pk': self.pk})
    
class Content(models.Model):
    module_associated = models.ForeignKey(module,on_delete=models.CASCADE)
    content_name = models.CharField(max_length=100)
    video = models.FileField(upload_to="course_content" ,validators=[video_validator],null=True,blank=True)
    description = models.TextField()
    is_description_content = models.BooleanField(default=0)
    studentCompleted = models.ManyToManyField(User,related_name="completed_student_content", blank=True, default=None)

    def __str__(self):
        return f'{str(self.module_associated.module_name)} - module content - {self.content_name}'



class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    course = models.ForeignKey(course, related_name='reviews',on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    user_name = models.ForeignKey(User, related_name='reviewers',on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)


    def __str__(self):
        return f'{self.course.course_name} by {self.user_name}'


class CourseCompleted(models.Model):
    courseid = models.ForeignKey(course,on_delete=models.CASCADE)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.userid} completed {self.courseid}' 

class ModuleCompleted(models.Model):
    moduleid = models.ForeignKey(module,on_delete=models.CASCADE)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.moduleid} completed by {self.userid}'

class contentCompleted(models.Model):
    contentid = models.ForeignKey(Content,on_delete=models.CASCADE)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.contentid} completed by {self.userid}'

class discussionpanel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100)
    description = models.TextField(blank = True , null = True)
    bloglike = models.ManyToManyField(User, related_name='discuss_posts_like', blank=True, default=None)

    def __str__(self):
        return f'{self.user} - question'

    def num_likes(self):
        return self.bloglike.count()


class discussionComment(models.Model):
    blog = models.ForeignKey(discussionpanel, related_name="comment_discuss", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    body = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f'{self.blog.user} - comment'