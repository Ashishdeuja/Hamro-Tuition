from datetime import date
from django.shortcuts import render, redirect, reverse, get_object_or_404
import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from teacher.models import Leave
from .forms import *
from .EmailBackend import EmailBackend
from django.contrib import messages
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import weasyprint
from django.views import generic
# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home_page"))
        elif request.user.user_type == '2':
            return redirect(reverse("teacher_home_page"))
        elif request.user_type == '3':
                return redirect(reverse("teacher_home_page"))
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
            elif user.user_type == '2':
                return redirect(reverse("teacher_home_page"))
            elif user.user_type == '3':
                return redirect(reverse("teacher_home_page"))
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
                return redirect(reverse('manage_class'))
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



def add_section(request):
    form = SectionForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Section'
    }
    if request.method == 'POST':
        if form.is_valid():
            section = form.cleaned_data.get('section')
            try:
                sections =Section()
                sections.section = section
                sections.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_section'))
            except:
                messages.error(request, "Error in adding the section")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'admin/add_section.html', context)

def manage_section(request):
    section = Section.objects.all()
    context = {
        'section': section,
        'page_title': 'Manage Section'
    }
    return render(request, "admin/manage_section.html", context)

def edit_section(request, section_id):
    instance = get_object_or_404(Section, id=section_id)
    form =SectionForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'section_id': section_id,
        'page_title': 'Edit Section'
    }
    if request.method == 'POST':
        if form.is_valid():
            section = form.cleaned_data.get('section')
            try:
                sections = Section.objects.get(id=section_id)
                sections.section = section
                sections.save()
                messages.success(request, "Section Successfully Updated")
                return redirect(reverse('manage_section'))
            except:
                messages.error(request, "Error while updating")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'admin/edit_section.html', context)

def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    try:
        section.delete()
        messages.success(request, "The section has been deleted successfully!")
    except Exception:
        messages.error(
            request, "The class couldn't be deleted !! ")
    return redirect(reverse('manage_section'))



def add_session(request):
    form = SessionForm(request.POST or None)
    context = {
        'form': form, 
        'page_title': 'Add Session'
        }
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Created")
                return redirect(reverse('add_session'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "admin/add_session.html", context)


def manage_session(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions, 'page_title': 'Manage Sessions'}
    return render(request, "admin/manage_session.html", context)

def edit_session(request, session_id):
    instance = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=instance)
    context = {
        'form': form, 
        'session_id': session_id,
        'page_title': 'Edit Session'
        }
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Updated")
                return redirect(reverse('edit_session', args=[session_id]))
            except Exception as e:
                messages.error(
                    request, "Session Could Not Be Updated " + str(e))
                return render(request, "admin/edit_session.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "admin/edit_session.html", context)

    else:
        return render(request, "admin/edit_session.html", context)



def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    try:
        session.delete()
        messages.success(request, "Session deleted successfully!")
    except Exception:
        messages.error(
            request, "There are students assigned to this session. Please move them to another session.")
    return redirect(reverse('manage_session'))


def add_subject(request):
    form = SubjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            code=form.cleaned_data.get('code')
            name = form.cleaned_data.get('subject_name')
            marks = form.cleaned_data.get('marks')
            level = form.cleaned_data.get('level')
            try:
                subject = Subject()
                subject.code=code
                subject.subject_name = name
                subject.marks = marks
                subject.level = level
                subject.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_subject'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'admin/add_subject.html', context)



def edit_subject(request, subject_id):
    instance = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'subject_id': subject_id,
        'page_title': 'Edit Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            code = form.cleaned_data.get('code')
            name = form.cleaned_data.get('subject_name')
            marks = form.cleaned_data.get('marks')
            level = form.cleaned_data.get('level')
            try:
                subject = Subject.objects.get(id=subject_id)
                subject.code=code
                subject.subject_name = name
                subject.marks = marks
                subject.level = level
                subject.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_subject', args=[subject_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'admin/edit_subject.html', context)


def manage_subject(request):
    subject = Subject.objects.all()
    context = {
        'subject': subject,
        'page_title': 'Manage Subject'
    }
    return render(request, "admin/manage_subject.html", context)

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    try:
        subject.delete()
        messages.success(request, "The subject has been deleted successfully!")
    except Exception:
        messages.error(
            request, "The subject couldn't be deleted !! ")
    return redirect(reverse('manage_subject'))


def subject_details(request, subject_id):
    subject_details = get_object_or_404(Subject, id=subject_id)
    context = {
        "subject_details": subject_details,
        'page_title': 'Subject Details'
    }
    return render(request, "admin/subject_details.html", context)



# def subject_details_pdf(request, subject_id):
#     subject = get_object_or_404(Subject, id=subject_id)
#     html = render_to_string('admin/subject_details.html',
#                             {'subject': subject})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename={subject.id}.pdf'
#     weasyprint.HTML(string=html).write_pdf(response,
#         stylesheets=[weasyprint.CSS(
#             settings.STATIC_ROOT + 'css/style.css')])
#     return response

def add_teacher(request):
    form = TeacherForm(request.POST or None, request.FILES or None)
    context = {
        'form': form, 
        'page_title': 'Add Teacher'
        }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            level = form.cleaned_data.get('level')
            subject = form.cleaned_data.get('subject')
            dob=form.cleaned_data.get('dob')
            phone_number=form.cleaned_data.get('phone_number')
            salary=form.cleaned_data.get('salary')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:

                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                    # email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url,address=address,gender=gender)
                # a=Level.objects.filter(level=level)[0]
                # tech=Teacher.objects.create(admin=user,level=a)
                # tech.save()
                # print(tech.query())
                
                user.gender = gender
                user.address = address
                user.dob=dob
                user.phone_number=phone_number
                user.teacher.salary=salary
                # a=Level.objects.filter(level=level)[0]
                # tech=Teacher.objects.create(admin=user,level=a)
                # tech.save()
                user.teacher.level= level
                user.teacher.subject= subject
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_teacher'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'admin/add_teacher.html', context)


def edit_teacher(request,teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    form = TeacherForm(request.POST or None, instance=teacher)
    context = {
        'form': form,
        'teacher_id':teacher_id, 
        'page_title': 'Edit Teacher'
        }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            level = form.cleaned_data.get('level')
            subject = form.cleaned_data.get('subject')
            dob=form.cleaned_data.get('dob')
            phone_number=form.cleaned_data.get('phone_number')
            salary=form.cleaned_data.get('salary')
            passport = request.FILES.get('profile_pic') or None
            # fs = FileSystemStorage()
            # filename = fs.save(passport.name, passport)
            # passport_url = fs.url(filename)
            try:

                user = CustomUser.objects.get(id=teacher.admin.id)
                user.email=email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                    
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                user.dob=dob
                user.phone_number=phone_number
                teacher.salary=salary
                teacher.level= level
                teacher.subject= subject
                user.save()
                teacher.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('edit_teacher',args=[teacher_id]))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")
    else:
        # user=CustomUser.objects.get(id=teacher_id)
        # teacher=Teacher.objects.get(id=user.id)

        return render(request, 'admin/edit_teacher.html', context)


def manage_teacher(request):
    teacher = CustomUser.objects.filter(user_type=2)
    context = {
        'teacher': teacher,
        'page_title': 'Manage Teacher'
    }
    return render(request, "admin/manage_teacher.html", context)

def delete_teacher(request, teacher_id):
    staff = get_object_or_404(CustomUser, teacher__id=teacher_id)
    staff.delete()
    messages.success(request, "Teacher deleted successfully!")
    return redirect(reverse('manage_teacher'))








# class FileView(generic.ListView):
#     model =Book
#     template_name = 'book/file.html'
#     context_object_name = 'books'

#     def get_queryset(self):
#     	return Book.objects.order_by('-id')
 

def manage_book(request):
    books = Book.objects.all()
    context = {
        'books': books,
        'page_title': 'Books'
    }
    return render(request, "book/file.html", context)

def add_book(request):
    form = BookForm(request.POST or None, request.FILES or None)
    context = {
        'form':form,
        'page_title':'Add Book'
    }
    if request.method == 'POST':
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            year = form.cleaned_data.get('year')
            publisher = form.cleaned_data.get('publisher')
            desc = form.cleaned_data.get('desc')
            cover = request.FILES.get('cover')
            pdf = request.FILES.get('pdf')
            try:
                
                book = Book()
                book.title=title 
                book.author=author
                book.year=year
                book.publisher=publisher
                book.desc=desc 
                book.cover=cover
                book.pdf=pdf
                book.save()
                messages.success(request, 'Book uploaded successfully')
                return redirect('manage_book')
            except Exception as e:
                 messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, 'Book not uploaded successfully')
    return render(request, 'book/add_book.html', context)


def edit_book(request, book_id):
    instance = get_object_or_404(Book, id=book_id)
    form = BookForm(request.POST or None, request.FILES or None, instance=instance)
    context = {
        'form': form,
        'book_id': book_id,
        'page_title': 'Edit Book'
    }
    if request.method == 'POST':
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            year = form.cleaned_data.get('year')
            publisher = form.cleaned_data.get('publisher')
            desc = form.cleaned_data.get('desc')
            cover = request.FILES.get('cover')
            pdf = request.FILES.get('pdf')
            try:
                book = Book.objects.get(id=book_id)
                book.title=title 
                book.author=author
                book.year=year
                book.publisher=publisher
                book.desc=desc 
                book.cover=cover
                book.pdf=pdf
                book.save()
                messages.success(request, (title + ' has been updated.'))
                return redirect('manage_book')
            except Exception as e:
                messages.error(request, "Could Not update " + str(e))
                
        else:
            messages.error(request, 'Please correct the error(s) below.')
    return render(request, 'book/edit_book.html',context)


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    title = book.title
    try:
        book.delete()
        messages.success(request, (title + ' has been deleted.'))
    except Exception:
        messages.error(request, "The book couldn't be deleted !!")
    return redirect('manage_book')

def add_student(request):
    student_form = StudentForm(request.POST or None, request.FILES or None)
    context = {
        'form': student_form, 
        'page_title': 'Add Student'
    }
    if request.method == 'POST':
        if student_form.is_valid():
            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            address = student_form.cleaned_data.get('address')
            email = student_form.cleaned_data.get('email')
            gender = student_form.cleaned_data.get('gender')
            password = student_form.cleaned_data.get('password')
            level = student_form.cleaned_data.get('level')
            section = student_form.cleaned_data.get('section')
            session = student_form.cleaned_data.get('session')
            dob=student_form.cleaned_data.get('dob')
            phone_number=student_form.cleaned_data.get('phone_number')
            fathers_name=student_form.cleaned_data.get('fathers_name')
            fathers_number=student_form.cleaned_data.get('fathers_number')
            mothers_name=student_form.cleaned_data.get('mothers_name')
            mothers_number=student_form.cleaned_data.get('mothers_number')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.dob=dob
                user.phone_number=phone_number
                user.student.fathers_name=fathers_name
                user.student.mothers_name=mothers_name
                user.student.fathers_number=fathers_number
                user.student.mothers_number=mothers_number
                user.student.session = session
                user.student.level = level
                user.student.section = section
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_student'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'admin/add_student.html', context)


def manage_student(request):
    student = CustomUser.objects.filter(user_type=3)
    context = {
        'student': student,
        'page_title': 'Manage student'
    }
    return render(request, "admin/manage_student.html", context)


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    context = {
        'form': form,
        'student_id': student_id,
        'page_title': 'Edit Student'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            level = form.cleaned_data.get('level')
            section = form.cleaned_data.get('section')
            session = form.cleaned_data.get('session')
            dob=form.cleaned_data.get('dob')
            phone_number=form.cleaned_data.get('phone_number')
            fathers_name=form.cleaned_data.get('fathers_name')
            fathers_number=form.cleaned_data.get('fathers_number')
            mothers_name=form.cleaned_data.get('mothers_name')
            mothers_number=form.cleaned_data.get('mothers_number')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=student.admin.id)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                student.section = section
                student.session = session
                user.gender = gender
                user.address = address
                user.dob=dob
                user.phone_number=phone_number
                user.fathers_name=fathers_name
                user.mothers_name=mothers_name
                user.fathers_number=fathers_number
                user.mothers_number=mothers_number
                student.level = level
                user.save()
                student.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_student', args=[student_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "admin/edit_student.html", context)


def delete_student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('manage_student'))



def admin_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
   
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
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
                custom_user = admin.admin
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
                return redirect(reverse('admin_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "admin/admin_profile.html", context)



def notice_view(request):
    items = NewsAndEvents.objects.all().order_by('-updated_date')
    context = {
        'items': items,
        'page_title': 'News and Events'
    }
    return render(request, 'admin/notice.html', context)


def add_notice(request):
    form = NewsAndEventsForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Notice'
    }
    if request.method == 'POST':
        if form.is_valid():
            title=form.cleaned_data.get('title')
            summary = form.cleaned_data.get('summary')
            posted_as = form.cleaned_data.get('posted_as')
            try:
                notice=NewsAndEvents()
                notice.title=title
                notice.summary=summary
                notice.posted_as=posted_as
                notice.save()
                messages.success(request, (title + ' has been uploaded.'))
                return redirect('view_notice')
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
                
        else:
            messages.error(request, 'Please correct the error(s) below.')
    return render(request, 'admin/add_notice.html',context)


def edit_notice(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    form = NewsAndEventsForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'pk': pk,
        'page_title': 'Edit Notice'
    }
    if request.method == 'POST':
        if form.is_valid():
            title=form.cleaned_data.get('title')
            summary = form.cleaned_data.get('summary')
            posted_as = form.cleaned_data.get('posted_as')
            try:
                notice=NewsAndEvents.objects.get(pk=pk)
                notice.title=title
                notice.summary=summary
                notice.posted_as=posted_as
                notice.save()
                messages.success(request, (title + ' has been updated.'))
                return redirect('view_notice')
            except Exception as e:
                messages.error(request, "Could Not update " + str(e))
                
        else:
            messages.error(request, 'Please correct the error(s) below.')
    return render(request, 'admin/edit_notice.html',context)



def delete_notice(request, pk):
    notice = get_object_or_404(NewsAndEvents, pk=pk)
    title = notice.title
    try:
        notice.delete()
        messages.success(request, (title + ' has been deleted.'))
    except Exception:
        messages.error(request, "The notice couldn't be deleted !!")
    return redirect('view_notice')


@csrf_exempt
def view_leave(request):
    if request.method != 'POST':
        allLeave = Leave.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications '
        }
        return render(request, "admin/view_leave.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(Leave, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False

@csrf_exempt
def check_email(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)
    
    