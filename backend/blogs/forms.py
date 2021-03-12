from django.forms import ModelForm
from .models import *

class commentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(commentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['placeholder'] = "Post a comment"
    
    class Meta:
        model = blogComment
        fields = ['body']

