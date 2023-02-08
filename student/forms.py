from django import forms
from django.forms.widgets import DateInput, TextInput
from administratior.forms import FormSettings
from .models import *

class TestimonialForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(TestimonialForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Testimonial
        fields = [ 'image', 'description']    