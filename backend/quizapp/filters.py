import django_filters
from .models import *

class quizFilter(django_filters.FilterSet):
    class Meta:
        model = quizcourse
        fields = ['title']
