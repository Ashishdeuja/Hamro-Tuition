import math
from django.db import models
from ckeditor.fields import RichTextField
from administratior.models import *

# Create your models here.
class Question(models.Model):
    choice=(
    ("Easy", "Easy"),
    ("Difficult", "Difficult"),
)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    question = models.CharField(max_length=400,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200)
    select_level = models.CharField(max_length = 30,choices =choice,default = '1')
    
    def __str__(self):
        return self.question
    
class Test_Resut(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_question=models.CharField(max_length=30)
    correct_ans=models.CharField(max_length=30)
    incorrect_ans=models.CharField(max_length=30)
    percentage=models.CharField(max_length=30)
    score=models.CharField(max_length=30)
    test_level=models.CharField(max_length=50)

class NoteRoom(models.Model):
    code = models.CharField(max_length = 10,default='0000000')
    level=models.ForeignKey(Level,on_delete=models.CASCADE)

    def __str__(self):
        return self.code

# class Image(models.Model):
#     images=models.ImageField(upload_to='notes/images/', null=True, blank=True)
     

class Notes(models.Model):
    title = models.CharField(max_length=200)
    # description = models.CharField(max_length=200)
    description=RichTextField()
    images=models.ImageField(upload_to='notes/images/', null=True, blank=True)
    # images = models.ManyToManyField(Image)
    file = models.FileField(upload_to='notes/pdfs/', null=True, blank=True) 
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    session = models.ForeignKey(Session,on_delete=models.CASCADE,null=True,blank=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    
    def __str__(self):
        return self.title


class Leave(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.CharField(max_length=60,blank=False,default='')
    end_date = models.CharField(max_length=60)
    reason =models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.reason

class Feedback(models.Model):
    message=models.TextField()
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    
class Attendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    present = models.BooleanField(default=False)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)     
 
