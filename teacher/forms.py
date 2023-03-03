from django import forms
from django.forms.widgets import DateInput, TextInput
from administratior.forms import FormSettings
from .models import *
from django.utils.translation import gettext_lazy as _

class QuestionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Question
        fields = ['select_level','question', 'op1', 'op2', 'op3', 'op4','ans'] 
        
class NoteForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args,**kwargs)
        

    class Meta:
        model=Notes
        fields=['title','description','images','file']
    
    
class LeaveForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                msg = _('End date cannot be earlier than start date')
                self.add_error('end_date', msg)

        return cleaned_data
    
    
    class Meta:
        model = Leave
        fields = ['start_date','end_date', 'reason']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }
        
