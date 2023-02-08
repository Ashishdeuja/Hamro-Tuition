from django import forms
from django.forms.widgets import DateInput, TextInput

from student.models import Testimonial

from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()
    dob=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number=forms.CharField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password','profile_pic', 'address','dob','phone_number' ]

class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields
        

class ClassForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['level']
        model = Level
        
class SectionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
    
    class Meta:
        fields=['section','level']
        model=Section    
    
class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['code','subject_name', 'marks', 'level']

class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'year': DateInput(attrs={'type': 'date'}),
        }


class TeacherForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Teacher
        fields = CustomUserForm.Meta.fields + \
            ['salary','level','subject' ]

class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
    
    class Meta(CustomUserForm.Meta):
        model=Student
        fields = CustomUserForm.Meta.fields + \
            ['fathers_name','fathers_number','mothers_name','mothers_number','level', 'session','section']

class BookForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'year', 'desc','cover','pdf']        


class NewsAndEventsForm(forms.ModelForm):
    class Meta:
        model = NewsAndEvents
        fields = ['title', 'summary', 'posted_as']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['posted_as'].widget.attrs.update({'class': 'form-control'})
        
        
        
class AboutForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(AboutForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = About
        fields = ['name', 'logo', 'home_image']    
        
class AboutPageForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(AboutPageForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = AboutPage
        fields = ['about_image', 'description'] 
        
class BODForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(BODForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = BOD
        fields = ['image','name','facebook_link','twiter_link','instagram_link','linkedin_link']    