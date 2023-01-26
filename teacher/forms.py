from django import forms
from django.forms.widgets import DateInput, TextInput
from administratior.forms import FormSettings
from .models import *

class QuestionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Question
        fields = ['subject','question', 'op1', 'op2', 'op3', 'op4','ans'] 
        
class NoteForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args,**kwargs)
        

    class Meta:
        model=Notes
        fields=['title','description','images','file']
    
    
class LeaveForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Leave
        fields = ['start_date','end_date', 'reason']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }