from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
import os 

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

class projects(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    video = models.FileField(upload_to='project/video/', validators=[video_validator])
    like = models.ManyToManyField(User, related_name='blog_posts', blank=True, default=None)

    def __str__(self):
        return f'{self.user} - project'

    def get_absolute_url(self):
        return reverse('project-list')

    
    def num_likes(self):
        return self.like.count()

class Comment(models.Model):
    project = models.ForeignKey(projects, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    body = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f'{self.project.user} - comment'
