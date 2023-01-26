from django.db import models
from ckeditor.fields import RichTextField
from administratior.models import *

# Create your models here.
class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING,null=True, blank=False)
    question = models.CharField(max_length=400,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
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
