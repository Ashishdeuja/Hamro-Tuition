from django.urls import path
from . import views

urlpatterns = [
    path("home/page", views.teacher_home_page, name='teacher_home_page'),
    path("profile", views.teacher_profile, name='teacher_profile'),
    
]