from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import RegexValidator
from recurit.models import language_category

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    languages_prefer = models.ManyToManyField(language_category,blank=True,default=None)
    rating = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user.username} Profile'  # this is to give the data in profile.html file


    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class teacher_profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    university_picture = models.ImageField(upload_to='university_pic',default='university.png')
    university_name = models.CharField(max_length = 100)
    position = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.user.username} - Teacher Profile'

class recruiter_profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    logo = models.ImageField(default='default.jpg',upload_to='profile_pics',null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    mobile_num_regex  = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    mobile_number  = models.CharField(validators=[mobile_num_regex], max_length=13, blank=True)


    def __str__(self):
        return f'{self.user} - company profile'
    
