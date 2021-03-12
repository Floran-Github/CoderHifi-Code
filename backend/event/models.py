from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here
class event(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='event/pic/')
    cost = models.IntegerField()
    last_day_of_registration = models.DateField(default=timezone.now)
    attend_link = models.CharField(max_length=500)
    userEnrolled = models.ManyToManyField(User,related_name="enrolled_user", blank=True, default=None)

    def __str__(self):
        return self.title   

    def get_absolute_url(self):
        return reverse('event-list')

class eventMaytoMany(models.Model):
    event_enroll_id = models.CharField(max_length=100)
    eventId = models.ForeignKey(event,related_name='eventmany',on_delete=models.CASCADE)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.userId} - enrolled in {self.eventId} : id no {self.event_enroll_id}'

