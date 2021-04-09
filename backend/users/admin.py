from django.contrib import admin
from .models import Profile,teacher_profile,recruiter_profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(teacher_profile)
admin.site.register(recruiter_profile)