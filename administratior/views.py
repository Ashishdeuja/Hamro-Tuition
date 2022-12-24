from django.shortcuts import render, redirect, reverse, get_object_or_404
import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .forms import *
from .EmailBackend import EmailBackend
from django.contrib import messages
from .models import *

# Create your views here.

def login_page(request):
    
    return render(request, 'login/login1.html')

def Login(request, **kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Login Denied</h4>")
    else:
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("admin_home_page"))
        else:   
            messages.error(request, "Enter the valid detalis")
            return redirect("/")
        

def Logout(request):
    if request.user != None:
        logout(request)
    return redirect("/")

def admin_home_page(request):
    context = {
        'page_title': "Home"
        
    }
    return render(request, 'admin/admin_home_page.html', context)
    

def add_class(request):
    form = ClassForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Class'
    }
    if request.method == 'POST':
        if form.is_valid():
            level = form.cleaned_data.get('level')
            try:
                classes =Level()
                classes.level = level
                classes.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_class'))
            except:
                messages.error(request, "Error in adding the class")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'admin/add_class.html', context)

def manage_class(request):
    level = Level.objects.all()
    context = {
        'level': level,
        'page_title': 'Manage Class'
    }
    return render(request, "admin/manage_class.html", context)

def edit_class(request, level_id):
    instance = get_object_or_404(Level, id=level_id)
    form =ClassForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'level_id': level_id,
        'page_title': 'Edit Class'
    }
    if request.method == 'POST':
        if form.is_valid():
            level = form.cleaned_data.get('level')
            try:
                classes = Level.objects.get(id=level_id)
                classes.level = level
                classes.save()
                messages.success(request, "Class Successfully Updated")
            except:
                messages.error(request, "Error while updating")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'admin/edit_class.html', context)

def delete_class(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    try:
        level.delete()
        messages.success(request, "The class has been deleted successfully!")
    except Exception:
        messages.error(
            request, "The class couldn't be deleted !! ")
    return redirect(reverse('manage_class'))