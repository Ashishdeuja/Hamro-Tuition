import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser




class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE = ((1, "Admin"), (2, "Teacher"), (3, "Student"))
    GENDER = [("M", "Male"), ("F", "Female")]
    
    
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    address = models.TextField()
    dob = models.DateField(null=True)
    phone_number = models.CharField(max_length=25,default="")
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    

class Level(models.Model):
    level = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.level
    
    
class Section(models.Model):
    section=models.CharField(max_length=22)
    # level=models.ForeignKey(Level, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.section
    

class Session(models.Model):
    year = models.DateField()

    def __str__(self):
        return str(self.year) 
 
class Subject(models.Model):
    code=models.CharField(max_length=10)
    subject_name=models.CharField(max_length=25)
    marks=models.IntegerField()
    level=models.ForeignKey(Level, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.subject_name
    

class Teacher(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # admin=None
    salary=models.IntegerField(null=True)
    level=models.ForeignKey(Level,on_delete=models.DO_NOTHING, null=True, blank=False)
    subject=models.ForeignKey(Subject,on_delete=models.DO_NOTHING, null=True)
    
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fathers_name=models.CharField(max_length=100)
    fathers_number = models.BigIntegerField(null=True)
    mothers_name = models.CharField(max_length=100)
    mothers_number = models.BigIntegerField(null=True)
    level=models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=False)
    section=models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
    
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
    

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000)
    pdf = models.FileField(upload_to='bookapp/pdfs/')
    cover = models.ImageField(upload_to='bookapp/covers/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs) 

class NewsAndEvents(models.Model):
    NEWS = "News"
    EVENTS = "Event"

    POST = (
        (NEWS, "News"),
        (EVENTS, "Event"),
    )
    
    title = models.CharField(max_length=200, null=True)
    summary = models.TextField(max_length=500, blank=True, null=True)
    posted_as = models.CharField(choices=POST, max_length=10)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class TimeTable(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_name = models.CharField(max_length=50)
    teacher = models.CharField(max_length=50)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Teacher.objects.create(admin=instance)
        if instance.user_type==3:
            Student.objects.create(admin=instance)
        


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.teacher.save()
    if instance.user_type==3:
        instance.student.save()
    


