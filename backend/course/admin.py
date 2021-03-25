from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Type_category)
admin.site.register(language_category)
admin.site.register(course)
admin.site.register(module)
admin.site.register(Content)
admin.site.register(Review)