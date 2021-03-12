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

class blogs(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank = True , null = True)
    image = models.ImageField(upload_to = 'blogs/pic/', blank = True , null = True)
    video = models.FileField(upload_to='blogs/video/', validators=[video_validator], blank = True , null = True)
    bloglike = models.ManyToManyField(User, related_name='blog_posts_like', blank=True, default=None)

    def __str__(self):
        return f'{self.user} - blog'

    def get_absolute_url(self):
        return reverse('blog-list')

    
    def num_likes(self):
        return self.bloglike.count()

class blogComment(models.Model):
    blog = models.ForeignKey(blogs, related_name="comment_blog", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    body = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f'{self.blog.user} - comment'