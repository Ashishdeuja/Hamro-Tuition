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
    level=models.ForeignKey(Level, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.section
    
    
class Subject(models.Model):
    code=models.CharField(max_length=10)
    name=models.CharField(max_length=25)
    marks=models.IntegerField()
    level=models.ForeignKey(Level, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    address=models.CharField(max_length=35)
    phone_number= models.CharField(max_length=25)
    gender=models.CharField(max_length=15)
    education=models.CharField(max_length=35)
    level=models.ForeignKey(Level,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Student(models.Model):
    name=models.CharField(max_length=40)
    email=models.EmailField()
    phone_number=models.CharField(max_length=15)
    address=models.CharField(max_length=30)
    gender=models.CharField(max_length=10)
    level=models.ForeignKey(Level, on_delete=models.CASCADE)
    section=models.ForeignKey(Section, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
    


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    


