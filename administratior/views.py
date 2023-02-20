import calendar
from datetime import date
from django.shortcuts import render, redirect, reverse, get_object_or_404
import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from teacher.models import *
from .forms import *
from .EmailBackend import EmailBackend
from django.contrib import messages
from .models import *
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import weasyprint
from django.views import generic
from django.db.models import Q
# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home_page"))
        elif request.user.user_type == '2':
            return redirect(reverse("teacher_home_page"))
        elif request.user.user_type == '3':
                return redirect(reverse("student_home_page"))
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
                return redirect(reverse("student_home_page"))
        else:   
            messages.error(request, "Enter the valid detalis")
            return redirect(reverse("loginpage"))
            # return redirect("/")
        

def Logout(request):
    if request.user != None:
        logout(request)
        # return redirect("/")
    return redirect(reverse("homepage"))

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
    
    query = request.GET.get('q')
    if query:
        level = level.filter(Q(level__icontains=query)).distinct()
        if not level:
            return render(request, "student/not_found.html")
    
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
        messages.error(request, "The class couldn't be deleted because some data may be assocated with it !! ")
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
            level = form.cleaned_data.get('level')
            try:
                sections =Section()
                sections.section = section
                sections.level=level
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
    
    query = request.GET.get('q')
    if query:
        section = section.filter(Q(section__icontains=query)|
                            Q(level__level__icontains=query)).distinct()
        if not section:
            return render(request, "student/not_found.html")
        
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
            level = form.cleaned_data.get('level')
            try:
                sections = Section.objects.get(id=section_id)
                sections.section = section
                sections.level=level
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
    query = request.GET.get('q')
    if query:
        subject = subject.filter(Q(subject_name__icontains=query)|
                                Q(code__icontains=query)|
                            Q(level__level__icontains=query)).distinct()
        if not subject:
            return render(request, "student/not_found.html")
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
    query = request.GET.get('q')
    if query:
        teacher = teacher.filter(Q(first_name__icontains=query)|
                                Q(first_name__icontains=query)|
                                Q(email__icontains=query)|
                                Q(address__icontains=query)|
                            Q(phone_number__icontains=query)).distinct()
        if not teacher:
            return render(request, "student/not_found.html")
        
    selected_status = request.GET.get('status')
    if selected_status:
        if selected_status == 'male':
            teacher =  teacher.filter(gender='M')
        elif selected_status == 'female':
            teacher =  teacher.filter(gender='F') 
    
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
    books = Book.objects.all().order_by('-updated_date')
    query = request.GET.get('q')
    if query:
        books = books.filter(Q(title__icontains=query) |
                                             Q(author__icontains=query) |
                                             Q(year__icontains=query) |
                                             Q(publisher__icontains=query)).distinct()
        if not books:
            return render(request, "student/not_found.html")
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
    query = request.GET.get('q')
    if query:
        student = student.filter(Q(first_name__icontains=query)|
                                Q(first_name__icontains=query)|
                                Q(email__icontains=query)|
                                Q(address__icontains=query)|
                                Q(dob__icontains=query)|
                            Q(phone_number__icontains=query)).distinct()
        if not student:
            return render(request, "student/not_found.html")
        
    selected_status = request.GET.get('status')
    if selected_status:
        if selected_status == 'male':
            student =  student.filter(gender='M')
        elif selected_status == 'female':
            student =  student.filter(gender='F') 
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


def get_subjects(request):
    level_id = request.GET.get('level')
    subjects = Subject.objects.filter(level_id=level_id)
    data = [{'id': s.id, 'name': s.subject_name} for s in subjects]
    return JsonResponse(data, safe=False)
    

def get_sections(request):
    level_id = request.GET.get('level')
    sections = Section.objects.filter(level_id=level_id)
    data = [{'id': s.id, 'name': s.section} for s in sections]
    return JsonResponse(data, safe=False)
    

def assign_teacher(request):
    form=AssignTeacherForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Assign Teacher'
    }
    if request.method == 'POST':
        if form.is_valid():
            level=form.cleaned_data.get('level')
            subject = form.cleaned_data.get('subject')
            teacher = form.cleaned_data.get('teacher')
            try:
                assign_teacher=AssignTeacher()
                assign_teacher.level=level
                assign_teacher.subject=subject
                assign_teacher.teacher=teacher
                assign_teacher.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('manage_assign_teacher'))
            except Exception as e:
                messages.error(request, "Error in adding the notes "+str(e))
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'admin/assign_teacher.html', context)

def edit_assign_teacher(request,assignteacher_id):
    instance = get_object_or_404(AssignTeacher, id=assignteacher_id)
    form=AssignTeacherForm(request.POST or None,instance=instance)
    context = {
        'form': form,
        'page_title': 'Assign Teacher'
    }
    if request.method == 'POST':
        if form.is_valid():
            level=form.cleaned_data.get('level')
            subject = form.cleaned_data.get('subject')
            teacher = form.cleaned_data.get('teacher')
            try:
                assign_teacher=AssignTeacher.objects.get(id=assignteacher_id)
                assign_teacher.level=level
                assign_teacher.subject=subject
                assign_teacher.teacher=teacher
                assign_teacher.save()
                messages.success(request, "Successfully Update")
                return redirect(reverse('manage_assign_teacher'))
            except Exception as e:
                messages.error(request, "Error in adding the notes "+str(e))
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'admin/edit_assign_teacher.html', context)


def manage_assign_teacher(request):
    assign_teacher =AssignTeacher.objects.all()
    query = request.GET.get('q')
    if query:
        assign_teacher = assign_teacher.filter(Q(subject__subject_name__icontains=query)|
                                Q(teacher__admin__first_name__icontains=query)|
                                Q(teacher__admin__last_name__icontains=query)|
                            Q(level__level__icontains=query)).distinct()
        if not assign_teacher:
            return render(request, "student/not_found.html")
    context = {
        'assign_teacher': assign_teacher,
        'page_title': 'Assigned Teachers'
    }
    return render(request, "admin/manage_assign_teacher.html", context)

def delete_assign_teacher(request, assignteacher_id):
    assign_teacher = get_object_or_404(AssignTeacher, id=assignteacher_id)
    try:
        assign_teacher.delete()
        messages.success(request, (' Assigned teacher has been removed.'))
    except Exception:
        messages.error(request, "The assigned teacher couldn't be removed !!")
    return redirect('manage_assign_teacher')




def admin_profile(request):
    admin = get_object_or_404(Admin, admin=request.user.id)
   
    form = AdminForm(request.POST or None, request.FILES or None, instance=admin)
    dob=admin.admin.dob
    today = date.today()
    if dob is not None:
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    else:
        age=0;    
    context = {'form': form,
               'page_title': 'Edit Profile',
               'age':age
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
                return redirect(reverse('loginpage'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "admin/admin_profile.html", context)



def notice_view(request):
    items = NewsAndEvents.objects.all().order_by('-updated_date')
    
    selected_status = request.GET.get('status')
    if selected_status:
        if selected_status == 'news':
            items =  items.filter(posted_as=NewsAndEvents.NEWS)
        elif selected_status == 'events':
            items =  items.filter(posted_as=NewsAndEvents.EVENTS) 
    context = {
        'items': items,
        'page_title': 'News and Events'
    }
    
    
    teachers = Teacher.objects.all()
    emails = [teacher.admin.email for teacher in teachers]
    numbers = [teacher.admin.phone_number for teacher in teachers]
    print(emails)
    print(numbers)
    
    students = Student.objects.all()
    semails = [student.admin.email for student in students]
    snumbers = [student.admin.phone_number for student in students]
    fnumbers = [str(student.fathers_number).replace(',', ';') for student in students if student.fathers_number]
    mnumbers = [student.mothers_number for student in students if student.mothers_number]
    print(semails)
    print(snumbers) 
    print(fnumbers)
    print(mnumbers)
    return render(request, 'admin/notice.html', context)


def add_notice(request):
    form = NewsAndEventsForm(request.POST or None)
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    first_name=request.user.first_name
    last_name=request.user.last_name
    student_emails = [student.admin.email for student in students]
    teacher_emails = [teacher.admin.email for teacher in teachers]
    
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
                email_from = "aasishdeuja@gmail.com"
                email_subject = title
                teacher_email_body="Dear Teachers,\n\n{0}.\n\nRegards,\n{1} {2}".format(summary,first_name,last_name)
                student_email_body = "Dear Students,\n\n{0}.\n\nRegards,\n{1} {2}".format(summary,first_name,last_name)

                try:
                    if teachers:
                        send_mail(email_subject,  teacher_email_body, email_from, teacher_emails, fail_silently=False)
                    if students:
                        send_mail(email_subject, student_email_body, email_from, student_emails, fail_silently=False)
                    messages.success(request, (title + ' has been uploaded.'))
                    return redirect('view_notice')
                except Exception:
                    messages.error(request, "Could not send email")
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
def teacher_check_leave(request):
    if request.method != 'POST':
        teacher=Teacher.objects.all()
        # teacher = get_object_or_404(Teacher)
        allLeave = Leave.objects.all()
        
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date and end_date:
            allLeave = allLeave.filter(start_date__range=[start_date, end_date])
            
            if not allLeave:
                return render(request, "student/not_found.html")
        
        query = request.GET.get('q')
        if query:
            allLeave = allLeave.filter(Q(reason__icontains=query) |
                                       Q(teacher__admin__first_name__icontains=query) |
                                       Q(teacher__admin__last_name__icontains=query) |
                                                Q(start_date__icontains=query) |
                                                Q(end_date__icontains=query)).distinct()
            if not allLeave:
                return render(request, "student/not_found.html")
            
        selected_status = request.GET.get('status')
        if selected_status:
            if selected_status == 'pending':
                 allLeave =  allLeave.filter(status=0)
            elif selected_status == 'approved':
                 allLeave =  allLeave.filter(status=1)
            elif selected_status == 'rejected':
                 allLeave =  allLeave.filter(status=-1)
                
        context = {
            'allLeave': allLeave,
            'teacher':teacher,
            'page_title': 'Leave Applications '
        }
        return render(request, "admin/view_leave.html", context)
    else:
        
        id = request.POST.get('id')
        status = request.POST.get('status')
        leave=Leave.objects.filter(id=id).select_related('teacher')
        email=leave[0].teacher.admin.email
        teacher_name=leave[0].teacher
        first_name=request.user.first_name
        last_name=request.user.last_name
        if (status == '1'):
            status = 1
            # leave=Leave.objects.filter(id=id).select_related('teacher')
            # print(leave[0].teacher.admin.email)
            # print(leave[0].teacher)
            # print(request.user.first_name)
            # print(request.user.last_name)
            
            email_to = email
            email_from = "aasishdeuja@gmail.com"
            email_subject = "Approved Leave Application"
            email_body = "Dear {0},\n\nI am writing to inform you that your leave application has been approved.\n\nRegards,\n{1} {2}".format(teacher_name,first_name,last_name)

            try:
                send_mail(email_subject, email_body, email_from, [email_to], fail_silently=False)
                messages.success(request, "The leave approved application has been sent to teacher.")
            except Exception:
                    messages.error(request, "Could not send email to teacher.")

                    return redirect(reverse('teacher_check_leave'))
        else:
            status = -1
            email_to = email
            email_from = "aasishdeuja@gmail.com"
            email_subject = "Rejected Leave Application"
            email_body = "Dear {0},\n\nI am writing to inform you that your leave application has been rejected.\n\nRegards,\n{1} {2}".format(teacher_name,first_name,last_name)

            try:
                send_mail(email_subject, email_body, email_from, [email_to], fail_silently=False)
                messages.success(request, "The leave rejected application has been sent to teacher.")
            except Exception:
                    messages.error(request, "Could not send email to teacher.")

                    return redirect(reverse('teacher_check_leave'))
        try:
            leave = get_object_or_404(Leave, id=id)
            leave.status = status
            leave.save()
            return redirect(reverse('teacher_check_leave'))
        except Exception as e:
            return False



@csrf_exempt
def student_check_leave(request):
    if request.method != 'POST':
        student=Student.objects.all()
        # teacher = get_object_or_404(Teacher)
        allLeave = Leave.objects.all()
        
        
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date and end_date:
            allLeave = allLeave.filter(start_date__range=[start_date, end_date])
            if not allLeave:
                return render(request, "student/not_found.html")
        
        query = request.GET.get('q')
        if query:
            allLeave = allLeave.filter(Q(reason__icontains=query) |
                                             Q(student__admin__first_name__icontains=query) |
                                            Q(student__admin__last_name__icontains=query) |
                                                Q(start_date__icontains=query) |
                                                Q(end_date__icontains=query)).distinct()
            if not allLeave:
                return render(request, "student/not_found.html")
        
        
        selected_status = request.GET.get('status')
        if selected_status:
            if selected_status == 'pending':
                 allLeave =  allLeave.filter(status=0)
            elif selected_status == 'approved':
                 allLeave =  allLeave.filter(status=1)
            elif selected_status == 'rejected':
                 allLeave =  allLeave.filter(status=-1)
                 
        context = {
            'allLeave': allLeave,
            'student':student,
            'page_title': 'Student Leave Applications '
        }
        return render(request, "admin/student_view_leave.html", context)
    else:
        
        id = request.POST.get('id')
        status = request.POST.get('status')
        leave=Leave.objects.filter(id=id).select_related('student')
        email=leave[0].student.admin.email
        student_name=leave[0].student
        first_name=request.user.first_name
        last_name=request.user.last_name
        if (status == '1'):
            status = 1
            # leave=Leave.objects.filter(id=id).select_related('teacher')
            # print(leave[0].teacher.admin.email)
            # print(leave[0].teacher)
            # print(request.user.first_name)
            # print(request.user.last_name)
            
            email_to = email
            email_from = "aasishdeuja@gmail.com"
            email_subject = "Approved Leave Application"
            email_body = "Dear {0},\n\nI am writing to inform you that your leave application has been approved.\n\nRegards,\n{1} {2}".format(student_name,first_name,last_name)

            try:
                send_mail(email_subject, email_body, email_from, [email_to], fail_silently=False)
                messages.success(request, "The leave approved application has been sent to student.")
            except Exception:
                    messages.error(request, "Could not send email to student.")

                    return redirect(reverse('student_check_leave'))
        else:
            status = -1
            email_to = email
            email_from = "aasishdeuja@gmail.com"
            email_subject = "Rejected Leave Application"
            email_body = "Dear {0},\n\nI am writing to inform you that your leave application has been rejected.\n\nRegards,\n{1} {2}".format(student_name,first_name,last_name)

            try:
                send_mail(email_subject, email_body, email_from, [email_to], fail_silently=False)
                messages.success(request, "The leave rejected application has been sent to student.")
            except Exception:
                    messages.error(request, "Could not send email to student.")

                    return redirect(reverse('student_check_leave'))
        try:
            leave = get_object_or_404(Leave, id=id)
            leave.status = status
            leave.save()
            return redirect(reverse('student_check_leave'))
        except Exception as e:
            return False



def view_timetable(request):
    timetable = TimeTable.objects.all()
    context = {'timetable': timetable}
    return render(request, 'admin/timetable.html', context)


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


    
def home(request):
    if request.method == 'POST':
        email_to = "aasishdeuja@gmail.com"
        email_from = "aasishdeuja@gmail.com"
        email_subject = "Enquiry by {0}".format(request.POST.get('name'))
        email_body = "Dear Administratior,\n\n{0}.\n\nRegards,\n{1}\n{2}".format(request.POST.get('message'),request.POST.get('name'),request.POST.get('email'))
        
        send_mail(email_subject, email_body, email_from, [email_to], fail_silently=False) 
        return redirect(reverse('homepage'))
    context = {
        'testimonial': Testimonial.objects.all(),
        'home':About.objects.all(),
        'about':AboutPage.objects.all(),
        'bod':BOD.objects.all(),
        'page_title': 'Testimonial'
    }
    return render(request,'admin/index.html',context)


@csrf_exempt
def testimonial(request):
    if request.method != 'POST':
        testimonials = Testimonial.objects.all()
        
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date and end_date:
            testimonials = testimonials.filter(created_at__range=[start_date, end_date])
            if not testimonials:
                return render(request, "student/not_found.html")
        
        query = request.GET.get('q')
        if query:
            testimonials = testimonials.filter(Q(description__icontains=query) |
                                             Q(student__admin__first_name__icontains=query) |
                                            Q(student__admin__last_name__icontains=query)).distinct()
            if not testimonials:
                return render(request, "student/not_found.html")
        
        selected_status = request.GET.get('status')
        if selected_status:
            if selected_status == 'pending':
                testimonials = testimonials.filter(status=0)
            elif selected_status == 'approved':
                testimonials = testimonials.filter(status=1)
            elif selected_status == 'rejected':
                testimonials = testimonials.filter(status=-1)
        context = {
            'testimonials': testimonials,
            # 'teacher':teacher,
            'page_title': 'Testimonials '
        }
        return render(request, "admin/view_testimonials.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(Testimonial, id=id)
            leave.status = status
            leave.save()
            return redirect('testimonial')
        except Exception as e:
            return False
        
def about_home(request):
    form = AboutForm(request.POST or None, request.FILES or None)
    context = {
        'form': form,
        'page_title': 'Home Page Content'
    }
    if request.method == 'POST':
        if form.is_valid():
            name=form.cleaned_data.get('name')
            logo = request.FILES.get('logo')
            home_image = request.FILES.get('home_image')
            try:
                home=About()
                home.name=name
                home.logo=logo
                home.home_image=home_image
                home.save()
                messages.success(request, (name + ' has been uploaded.'))
                return redirect('manage_home_page')
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
                
        else:
            messages.error(request, 'Please correct the error(s) below.')
    return render(request, 'admin/add_home.html',context)

def edit_home(request, pk):
    instance = get_object_or_404(About, pk=pk)
    form = AboutForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'pk': pk,
        'page_title': 'Edit Home Page Content'
    }
    if request.method == 'POST':
        if form.is_valid():
            name=form.cleaned_data.get('name')
            logo = request.FILES.get('logo')
            home_image = request.FILES.get('home_image')
            try:
                home=About()
                home.name=name
                home.logo=logo
                home.home_image=home_image
                home.save()
                messages.success(request, (name + ' has been uploaded.'))
                return redirect('manage_home_page')
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
                
        else:
            messages.error(request, 'Please correct the error(s) below.')
    return render(request, 'admin/edit_home.html',context)


def delete_home(request, pk):
    home = get_object_or_404(About, pk=pk)
    try:
        home.delete()
        messages.success(request, ('Home content has been deleted.'))
    except Exception:
        messages.error(request, "The home content couldn't be deleted !!")
    return redirect('manage_home_page')


def manage_home_page(request):
    
    context = {
       
        'home': About.objects.all(),
        'page_title': 'Home Content'
    }
    return render(request, "admin/manage_home.html", context)


def aboutpage_home(request):
    form = AboutPageForm(request.POST or None, request.FILES or None)
    context = {
        'form': form,
        'page_title': 'About Page Content'
    }
    if request.method == 'POST':
        if form.is_valid():
            about_image = request.FILES.get('about_image')
            description = form.cleaned_data.get('description')
            try:
                about=AboutPage()
                about.about_image=about_image
                about.description=description
                about.save()
                messages.success(request, ('About Content has been uploaded.'))
                return redirect('manage_about_page')
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
                
        else:
            messages.error(request, 'Please correct the error(s) below.')
    return render(request, 'admin/add_about.html',context)


def manage_about_page(request):
    
    context = {
       
        'abouts': AboutPage.objects.all(),
        'page_title': 'About Content'
    }
    return render(request, "admin/manage_about.html", context)

def edit_about(request, pk):
    instance = get_object_or_404(AboutPage, pk=pk)
    form = AboutPageForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'pk': pk,
        'page_title': 'Edit About Page Content'
    }
    if request.method == 'POST':
        if form.is_valid():
            about_image = request.FILES.get('about_image')
            description = form.cleaned_data.get('description')
            try:
                about=AboutPage.objects.get(pk=pk)
                about.about_image=about_image
                about.description=description
                about.save()
                messages.success(request, ('About Content has been updated.'))
                return redirect('manage_about_page')
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
                
        else:
            messages.error(request, 'Please correct the error(s) below.')
    return render(request, 'admin/edit_home.html',context)

def delete_about(request, pk):
    about = get_object_or_404(AboutPage, pk=pk)
    try:
        about.delete()
        messages.success(request, ('About content has been deleted.'))
    except Exception:
        messages.error(request, "The about content couldn't be deleted !!")
    return redirect('manage_about_page')


def bod_page(request):
    form = BODForm(request.POST or None, request.FILES or None)
    context = {
        'form': form,
        'page_title': 'BOD Page Content'
    }
    if request.method == 'POST':
        if form.is_valid():
            image = request.FILES.get('image')
            name=form.cleaned_data.get('name')
            facebook_link = form.cleaned_data.get('facebook_link')
            twiter_link = form.cleaned_data.get('twiter_link')
            instagram_link = form.cleaned_data.get('instagram_link')
            linkedin_link = form.cleaned_data.get('linkedin_link')
            try:
                bod=BOD()
                bod.image=image
                bod.name=name
                bod.facebook_link=facebook_link
                bod.instagram_link=instagram_link
                bod.twiter_link=twiter_link
                bod.linkedin_link=linkedin_link
                bod.save()
                messages.success(request, ('BOD Content has been uploaded.'))
                return redirect('manage_bod_page')
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
                
        else:
            messages.error(request, 'Please correct the error(s) below.')
    return render(request, 'admin/add_bod.html',context)


def manage_bod_page(request):
    
    context = {
       
        'bod': BOD.objects.all(),
        'page_title': 'BOD Content'
    }
    return render(request, "admin/manage_bod.html", context)


def edit_bod_page(request,pk):
    instance = get_object_or_404(BOD, pk=pk)
    form = BODForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'pk': pk,
        'page_title': 'Edit About Page Content'
    }
    if request.method == 'POST':
        if form.is_valid():
            image = request.FILES.get('image')
            name=form.cleaned_data.get('name')
            facebook_link = form.cleaned_data.get('facebook_link')
            twiter_link = form.cleaned_data.get('twiter_link')
            instagram_link = form.cleaned_data.get('instagram_link')
            linkedin_link = form.cleaned_data.get('linkedin_link')
            try:
                bod=BOD.objects.get(pk=pk)
                bod.image=image
                bod.name=name
                bod.facebook_link=facebook_link
                bod.instagram_link=instagram_link
                bod.twiter_link=twiter_link
                bod.linkedin_link=linkedin_link
                bod.save()
                messages.success(request, ('BOD Content has been updated.'))
                return redirect('manage_bod_page')
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
                
        else:
            messages.error(request, 'Please correct the error(s) below.')
    return render(request, 'admin/edit_home.html',context)

def delete_bod(request, pk):
    bod = get_object_or_404(BOD, pk=pk)
    try:
        bod.delete()
        messages.success(request, ('BOD content has been deleted.'))
    except Exception:
        messages.error(request, "The bod content couldn't be deleted !!")
    return redirect('manage_bod_page')

def admin_view_attendance(request):
    level = Level.objects.all()
    context = {
        'level':level,
        'page_title': 'Attendance'
    }
    return render(request, "admin/manage_attendance.html", context)

def manage_attendance_section(request,level_id):
    section = Section.objects.filter(level=level_id)
    level=Level.objects.get(id=level_id)
    context = {
        'section':section,
        'page_title': 'Attendance of {0}'.format(level)
    }
    return render(request, "admin/manage_attendance_section.html", context)


def section_view_students_attendance(request,section_id):
    # student= Student.objects.all()
    # students = Student.objects.filter(section=section_id)
    student=Student.objects.filter(section=section_id)
    section = Section.objects.get(id=section_id)
    
    context = {
        'student':student,
        'section_id':section_id,
        'page_title': 'Attendance of {0}'.format(section)
    }

    return render(request, "admin/students.html", context)


def admin_attendance_view(request,student_id):
    student= get_object_or_404(Student, id=student_id)
    attendance = Attendance.objects.filter(student=student).order_by('-date')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
        
    if start_date and end_date:
            attendance = attendance.filter(date__range=[start_date, end_date])
            
            if not attendance:
                return render(request, "student/not_found.html")
    
    status = request.GET.get('status')
    if status == 'present':
        attendance = attendance.filter(present=True)
    elif status == 'absent':
        attendance = attendance.filter(present=False)
    
    attendance_by_month = {}
    for record in attendance:
        month = record.date.strftime("%B %Y")
        if month not in attendance_by_month:
            attendance_by_month[month] = []
        attendance_by_month[month].append(record)

    attendance_by_month_items = list(attendance_by_month.items())
    paginator = Paginator(attendance_by_month_items, 1) # show 1 month per page
    page = request.GET.get('page')
    attendance_by_month_paginated = paginator.get_page(page)
    context = {
        'attendance_by_month_paginated':attendance_by_month_paginated,
        'page_title': 'Attendance'
    }
    return render(request, "attendance/student_view_attendance.html", context)


def attendance_pdf(request,student_id):
    student= get_object_or_404(Student, id=student_id)
    attendance = Attendance.objects.filter(student=student).order_by('-date')
    attendance_by_month = {}
    for record in attendance:
        month = record.date.strftime("%B %Y")
        if month not in attendance_by_month:
            attendance_by_month[month] = []
        attendance_by_month[month].append(record)
    context = {
        'attendance_by_month':attendance_by_month,
        'student':student,
        'page_title': 'Attendance'
    }
    template = get_template("attendance/student_view_attendance_pdf.html")
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    filename = f"{student}_Monthly_Attendance_Report.pdf"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    pisaStatus = pisa.CreatePDF(html, dest=response)

    if pisaStatus.err:
        return HttpResponse("PDF creation error: {0}".format(pisaStatus.err))
    else:
        return response

def view_daily_attendance_pdf(request,student_id):
    student = get_object_or_404(Student,id=student_id)
    attendance = Attendance.objects.filter(student=student).order_by('-date')
    attendance_by_day = {}
    for record in attendance:
        day = record.date.strftime("%Y-%m-%d")
        if day not in attendance_by_day:
            attendance_by_day[day] = []
        attendance_by_day[day].append(record)
    context = {
        'attendance_by_day': attendance_by_day,
        'student': student,
        'page_title': 'Attendance'
    }
    
    template = get_template("attendance/daily_attendance_pdf.html")
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    filename = f"{student}_Daily_Attendance_Report.pdf"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    pisaStatus = pisa.CreatePDF(html, dest=response)

    if pisaStatus.err:
        return HttpResponse("PDF creation error: {0}".format(pisaStatus.err))
    else:
        return response
    # return render(request, 'attendance/daily_attendance_pdf.html', context)
    
def view_weekly_attendance_pdf(request,student_id):
    student = get_object_or_404(Student, id=student_id)
    attendance = Attendance.objects.filter(student=student).order_by('-date')
    attendance_by_week = {}
    for record in attendance:
        week_start = record.date - datetime.timedelta(days=record.date.weekday()+1)
        week_end = week_start + datetime.timedelta(days=6)
        if record.date.weekday() == 6:
            next_week_start = week_end + datetime.timedelta(days=1)
            next_week_end = next_week_start + datetime.timedelta(days=6)
            week = f"{next_week_start.strftime('%Y-%m-%d')} to {next_week_end.strftime('%Y-%m-%d')}"
            if week not in attendance_by_week:
                attendance_by_week[week] = []
            attendance_by_week[week].append(record)
        else:
            week = f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}"
            if week not in attendance_by_week:
                attendance_by_week[week] = []
            attendance_by_week[week].append(record)
            
    context = {
        'attendance_by_week': attendance_by_week,
        'student': student,
        'page_title': 'Attendance'
    }
    
    template = get_template("attendance/weekly_attendance_pdf.html")
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    filename = f"{student}_Weekly_Attendance_Report.pdf"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    pisaStatus = pisa.CreatePDF(html, dest=response)

    if pisaStatus.err:
        return HttpResponse("PDF creation error: {0}".format(pisaStatus.err))
    else:
        return response
    # return render(request, 'attendance/weekly_attendance_pdf.html', context)

def view_yearly_attendance_pdf(request,student_id):
    student = get_object_or_404(Student, id=student_id)
    attendance = Attendance.objects.filter(student=student).order_by('date')
    year = datetime.datetime.now().year
    attendance_by_month = {}
    total_days = 0
    present_days = 0
    absent_days = 0
    for record in attendance:
        month = record.date.strftime("%B")
        if month not in attendance_by_month:
            attendance_by_month[month] = {
                'total_days': 0,
                'present_days': 0,
                'absent_days': 0,
            }
        attendance_by_month[month]['total_days'] += 1
        total_days += 1
        if record.present==True:
            attendance_by_month[month]['present_days'] += 1
            present_days += 1
        else:
            attendance_by_month[month]['absent_days'] += 1
            absent_days += 1

    context = {
        'year': year,
        'attendance_by_month': attendance_by_month,
        'student': student,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'page_title': 'Yearly Attendance Report'
    }
    template = get_template("attendance/yearly_attendance_pdf.html")
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    filename = f"{student}_Yearly_Attendance_Report.pdf"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    pisaStatus = pisa.CreatePDF(html, dest=response)

    if pisaStatus.err:
        return HttpResponse("PDF creation error: {0}".format(pisaStatus.err))
    else:
        return response
    # return render(request, 'attendance/yearly_attendance_pdf.html', context)

def admin_view_all_attendance(request,section_id):
    students = Student.objects.filter(section=section_id)
    attendance = Attendance.objects.filter(section=section_id).order_by('-date')
    section = Section.objects.get(id=section_id)
    attendance_by_month = {}
    for record in attendance:
        month = record.date.strftime("%B %Y")
        if month not in attendance_by_month:
            attendance_by_month[month] = []
        attendance_by_month[month].append(record)

    attendance_by_month_items = list(attendance_by_month.items())
    paginator = Paginator(attendance_by_month_items, 1) # show 1 month per page
    page = request.GET.get('page')
    attendance_by_month_paginated = paginator.get_page(page)
    
    
    
    context = {
        'students': students,
        'attendance': attendance,
        'section_id':section_id,
        # 'attendance_id':attendance_id,
        'attendance_by_month_paginated': attendance_by_month_paginated,
        'page_title': 'Attendance of {0} Section {1}'.format(section.level,section)
    }
    
    return render(request, "attendance/view_attendance.html", context)



def admin_download_all_attendance(request,section_id):
    students = Student.objects.filter(section=section_id)
    attendance = Attendance.objects.filter(section=section_id).order_by('-date')
    section = Section.objects.get(id=section_id)
    attendance_by_month = {}
    for record in attendance:
        month = record.date.strftime("%B %Y")
        if month not in attendance_by_month:
            attendance_by_month[month] = []
        attendance_by_month[month].append(record)
       
    
    context = {
        'students': students,
        'attendance': attendance,
        'section_id':section_id,
        # 'attendance_id':attendance_id,
        'attendance_by_month': attendance_by_month,
        'page_title': 'Attendance of {0} Section {1}'.format(section.level,section)
    }
    template = get_template("attendance/download_all_attendance.html")
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    filename = f"{section.level}_section_{section}_Attendance_Report.pdf"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    pisaStatus = pisa.CreatePDF(html, dest=response)
    if pisaStatus.err:
        return HttpResponse("PDF creation error: {0}".format(pisaStatus.err))
    else:
        return response
    
    

def daily_all_attendance_pdf(request,section_id):
    students = Student.objects.filter(section=section_id)
    attendance = Attendance.objects.filter(section=section_id).order_by('-date')
    section = Section.objects.get(id=section_id)
    attendance_by_day = {}
    for record in attendance:
        day = record.date.strftime("%Y-%m-%d")
        if day not in attendance_by_day:
            attendance_by_day[day] = []
        attendance_by_day[day].append(record)
    context = {
        'attendance_by_day': attendance_by_day,
        'students': students,
        'section_id':section_id,
        'page_title': 'Daily Attendance of {0} Section {1}'.format(section.level,section)
    }
    
    template = get_template("attendance/daily_all_attendance.html")
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    filename = f"{section.level}_section_{section}_Daily_Attendance_Report.pdf"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    pisaStatus = pisa.CreatePDF(html, dest=response)

    if pisaStatus.err:
        return HttpResponse("PDF creation error: {0}".format(pisaStatus.err))
    else:
        return response
    # return render(request, 'attendance/daily_attendance_pdf.html', context)
    
def weekly_all_attendance_pdf(request,section_id):
    students = Student.objects.filter(section=section_id)
    attendance = Attendance.objects.filter(section=section_id).order_by('-date')
    section = Section.objects.get(id=section_id)
    attendance_by_week = {}
    for record in attendance:
        week_start = record.date - datetime.timedelta(days=record.date.weekday()+1)
        week_end = week_start + datetime.timedelta(days=6)
        if record.date.weekday() == 6:
            next_week_start = week_end + datetime.timedelta(days=1)
            next_week_end = next_week_start + datetime.timedelta(days=6)
            week = f"{next_week_start.strftime('%Y-%m-%d')} to {next_week_end.strftime('%Y-%m-%d')}"
            if week not in attendance_by_week:
                attendance_by_week[week] = []
            attendance_by_week[week].append(record)
        else:
            week = f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}"
            if week not in attendance_by_week:
                attendance_by_week[week] = []
            attendance_by_week[week].append(record)      
    context = {
        'attendance_by_week': attendance_by_week,
        'students': students,
        'page_title': 'Weekly Attendance of {0} Section {1}'.format(section.level,section)
    }
    
    template = get_template("attendance/weekly_all_attendance.html")
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    filename = f"{section.level}_section_{section}_Weekly_Attendance_Report.pdf"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    pisaStatus = pisa.CreatePDF(html, dest=response)

    if pisaStatus.err:
        return HttpResponse("PDF creation error: {0}".format(pisaStatus.err))
    else:
        return response
    # return render(request, 'attendance/weekly_attendance_pdf.html', context)

# def yearly_all_attendance_pdf(request,section_id):
    # student = Student.objects.filter(section=section_id)
    # attendance = Attendance.objects.all().order_by('date')
    # section = Section.objects.get(id=section_id)
    # year = datetime.datetime.now().year
    # attendance_by_month = {}
    # total_days = 0
    # present_days = 0
    # absent_days = 0
    # for record in attendance:
    #     month = record.date.strftime("%B")
    #     if month not in attendance_by_month:
    #         attendance_by_month[month] = {
    #             'total_days': 0,
    #             'present_days': 0,
    #             'absent_days': 0,
    #         }
    #     attendance_by_month[month]['total_days'] += 1
    #     total_days += 1
    #     if record.present==True:
    #         attendance_by_month[month]['present_days'] += 1
    #         present_days += 1
    #     else:
    #         attendance_by_month[month]['absent_days'] += 1
    #         absent_days += 1

    # context = {
    #     'year': year,
    #     'attendance_by_month': attendance_by_month,
    #     'student': student,
    #     'total_days': total_days,
    #     'present_days': present_days,
    #     'absent_days': absent_days,
    #     'page_title': 'Yearly Attendance of {0} Section {1}'.format(section.level,section)
    # }
    # # template = get_template("attendance/yearly_all_attendance.html")
    # # html = template.render(context)
    # # response = HttpResponse(content_type='application/pdf')
    # # filename = f"{section.level}_section_{section}_Yearly_Attendance_Report.pdf"
    # # response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    # # pisaStatus = pisa.CreatePDF(html, dest=response)

    # # if pisaStatus.err:
    # #     return HttpResponse("PDF creation error: {0}".format(pisaStatus.err))
    # # else:
    # #     return response
    
def yearly_all_attendance_pdf(request, section_id):
    students = Student.objects.filter(section=section_id)
    attendances = Attendance.objects.all()
    section = Section.objects.get(id=section_id)
    year = datetime.datetime.now().year
    # attendance_by_month = {}
    # for record in attendances:
    #     month = record.date.strftime("%B")
    #     if month not in attendance_by_month:
    #         attendance_by_month[month] = {}
    #     for student in students:
    #         if student.id not in attendance_by_month[month]:
    #             attendance_by_month[month][student.id] = {
    #                 'total_days': 0,
    #                 'present_days': 0,
    #                 'absent_days': 0,
    #             }
    #         if record.student == student:
    #             attendance_by_month[month][student.id]['total_days'] += 1
    #             if record.present:
    #                 attendance_by_month[month][student.id]['present_days'] += 1
    #             else:
    #                 attendance_by_month[month][student.id]['absent_days'] += 1

    # table_rows = []
    # for student in students:
    #     total_days = 0
    #     present_days = 0
    #     absent_days = 0
    #     month_data = []
    #     for month, attendance in attendance_by_month.items():
    #         month_total_days = attendance[student.id]['total_days']
    #         month_present_days = attendance[student.id]['present_days']
    #         month_absent_days = attendance[student.id]['absent_days']
    #         month_data.append({
    #             'month': month,
    #             'total_days': month_total_days,
    #             'present_days': month_present_days,
    #             'absent_days': month_absent_days,
    #         })
    #         total_days += month_total_days
    #         present_days += month_present_days
    #         absent_days += month_absent_days


    #     if total_days == 0:
    #         attendance_percentage = 0
    #     else:
    #         attendance_percentage = round((present_days / total_days) * 100, 2)
            
       
    #     table_rows.append({
    #         'student': student,
    #         'total_days': total_days,
    #         'present_days': present_days,
    #         'absent_days': absent_days,
    #         'month_data': month_data,
    #         'percentage': attendance_percentage,
    #     })
    
    
    # context = {
    #     'year': year,
    #     'table_rows': table_rows,
    #     'attendance_by_month': attendance_by_month,
    #     'page_title': 'Yearly Attendance of {0} Section {1}'.format(section.level, section),
    # }
    # print(table_rows)
    
    
    
    attendance_by_month = {}
    for record in attendances:
        month = record.date.strftime("%B")
        if month not in attendance_by_month:
            attendance_by_month[month] = {}
        for student in students:
            if student.id not in attendance_by_month[month]:
                attendance_by_month[month][student.id] = {
                    'total_days': 0,
                    'present_days': 0,
                    'absent_days': 0,
                }
            if record.student == student:
                attendance_by_month[month][student.id]['total_days'] += 1
                if record.present:
                    attendance_by_month[month][student.id]['present_days'] += 1
                else:
                    attendance_by_month[month][student.id]['absent_days'] += 1

    attendance_by_month_sorted = dict(sorted(attendance_by_month.items(), key=lambda x: datetime.datetime.strptime(x[0], '%B')))

    table_rows = []
    for student in students:
        total_days = 0
        present_days = 0
        absent_days = 0
        month_data = []
        for month, attendance in attendance_by_month_sorted.items():
            month_total_days = attendance[student.id]['total_days']
            month_present_days = attendance[student.id]['present_days']
            month_absent_days = attendance[student.id]['absent_days']
            month_data.append({
                'month': month,
                'total_days': month_total_days,
                'present_days': month_present_days,
                'absent_days': month_absent_days,
            })
            total_days += month_total_days
            present_days += month_present_days
            absent_days += month_absent_days


        if total_days == 0:
            attendance_percentage = 0
        else:
            attendance_percentage = round((present_days / total_days) * 100, 2)


        table_rows.append({
            'student': student,
            'total_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'month_data': month_data,
            'percentage': attendance_percentage,
        })
    context = {
        'year': year,
        'table_rows': table_rows,
        'attendance_by_month': attendance_by_month_sorted,
        'page_title': 'Yearly Attendance of {0} Section {1}'.format(section.level, section),
    }
    
    
    template = get_template("attendance/yearly_all_attendance.html")
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    filename = f"{section.level}_section_{section}_Yearly_Attendance_Report.pdf"
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    pisaStatus = pisa.CreatePDF(html, dest=response)

    if pisaStatus.err:
        return HttpResponse("PDF creation error: {0}".format(pisaStatus.err))
    else:
        return response
    # return render(request, 'attendance/yearly_all_attendance.html', context)