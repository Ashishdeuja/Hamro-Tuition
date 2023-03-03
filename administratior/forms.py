from datetime import date
from django import forms
from django.forms.widgets import DateInput, TextInput
from django.core.validators import MinValueValidator, MaxValueValidator
from student.models import Testimonial

from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

PHONE_REGEX = r'^\+?[0-9]{8,16}$'

phone_validator = RegexValidator(
    regex=PHONE_REGEX,
    message='Please enter a valid phone number'
)


class PhoneFormField(forms.CharField):
    default_validators = [phone_validator]

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
    phone_number = PhoneFormField(max_length=16)
    
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
        
    year = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    class Meta:
        model = Session
        fields = '__all__'
        
class TeacherForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)

    def clean_dob(self):
        dob = self.cleaned_data['dob']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        if dob > today:
            raise ValidationError('Date of birth cannot be in the future')
        elif age < 18:
            raise ValidationError('The teacher must be at least 18 years old to get registered.')
        return dob

    class Meta(CustomUserForm.Meta):
        model = Teacher
        fields = CustomUserForm.Meta.fields + \
            ['salary' ]
            
            
class AssignTeacherForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(AssignTeacherForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = AssignTeacher
        fields = ['level','subject','teacher']

class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        
    def clean_dob(self):
        dob = self.cleaned_data['dob']
        if dob > datetime.today().date():
            raise ValidationError('Invalid date of birth')
        return dob
    
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
        fields = ['name','image','facebook_link','twiter_link','instagram_link','linkedin_link']    