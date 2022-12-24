from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name='loginpage'),
    path("Login/", views.Login, name='login'),
    path("Logout/", views.Logout, name='logout'),
    path("admin/home/", views.admin_home_page, name='admin_home_page'),
    path("add/class/", views.add_class, name='add_class'),
    path("manage/class/", views.manage_class, name='manage_class'),
    path("edit/class/<int:level_id>", views.edit_class, name='edit_class'),
    path("delete/class/<int:level_id>", views.delete_class, name='delete_class'),
    
   

]