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
    question = models.CharField(max_length=400,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200)
    select_level = models.CharField(max_length = 30,choices =choice,default = '1')
    
    def __str__(self):
        return self.question

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
    
    
class Bookmark(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)