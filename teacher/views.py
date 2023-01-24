from django.shortcuts import render,get_object_or_404,redirect,reverse

from administratior.forms import *
from administratior.models import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Create your views here.
def teacher_home_page(request):
    context = {
        'page_title': "Dashboard"
        
    }
    return render(request, 'teacher/teacher_home_page.html', context)

def teacher_profile(request):
    teacher = get_object_or_404(Teacher, admin=request.user)
   
    form = TeacherForm(request.POST or None, request.FILES or None, instance=teacher)
    # dob=admin.dob
    # today = date.today()
    # age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    context = {'form': form,
               'page_title': 'Edit Profile',
            #    'age':age
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                dob=form.cleaned_data.get('dob')
                phone_number=form.cleaned_data.get('phone_number')
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                # today = date.today()
                # age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = teacher.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.dob=dob
                custom_user.phone_number=phone_number
                custom_user.address=address
                custom_user.gender=gender
                # custom_user.age=age
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('teacher_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "teacher/teacher_profile.html", context)