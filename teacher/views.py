from datetime import date, timezone
from http.client import HTTPResponse
import json
from django.shortcuts import render,get_object_or_404,redirect,reverse
from .forms import *
from django.core.mail import send_mail
from administratior.forms import *
from administratior.models import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q
import re
from django.contrib.auth.hashers import check_password
# Create your views here.
def teacher_home_page(request):
    context = {
        'page_title': "Dashboard"
        
    }
    return render(request, 'teacher/teacher_home_page.html', context)

def validate_password(password):
    if len(password) < 8:
        raise forms.ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise forms.ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise forms.ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        raise forms.ValidationError("Password must contain at least one digit.")

def teacher_profile(request):
    teacher = get_object_or_404(Teacher, admin=request.user)
   
    form = TeacherForm(request.POST or None, request.FILES or None, instance=teacher)
    dob=teacher.admin.dob
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
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
                salary = form.cleaned_data.get('salary')
                # today = date.today()
                # age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                
                # if password != None:
                #     try:
                #         validate_password(password)
                #     except forms.ValidationError as e:
                #         form.add_error('password', e)
                #         raise forms.ValidationError("Invalid Password")

                custom_user = teacher.admin
                if password != None:
                    if check_password(password, custom_user.password):
                        messages.error(request, "New password should be different from current password")
                        return redirect(reverse('teacher_profile'))
                    else:
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
                custom_user.teacher.salary=salary
                # custom_user.age=age
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('teacher_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))
    return render(request, "teacher/teacher_profile.html", context)


def add_question(request,subject_id):
    form = QuestionForm(request.POST or None)
    # teacher = get_object_or_404(Teacher, admin=request.user)
    # subjects = Subject.objects.filter(teacher=teacher)
    context = {
        'form': form,
        # 'subjects': subjects,
        'page_title': 'Add Question'
    }
    if request.method == 'POST':
        if form.is_valid():
            question = form.cleaned_data.get('question')
            select_level=form.cleaned_data.get('select_level')
            opt1=form.cleaned_data.get('op1')
            opt2=form.cleaned_data.get('op2')
            opt3=form.cleaned_data.get('op3')
            opt4=form.cleaned_data.get('op4')
            ans=form.cleaned_data.get('ans')
            try:
                questions =Question()
                subject=Subject(pk=subject_id)
                questions.subject=subject
                questions.select_level=select_level
                questions.question=question
                questions.op1=opt1
                questions.op2=opt2
                questions.op3=opt3
                questions.op4=opt4
                questions.ans=ans 
                questions.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('view_questions', args=[subject_id]))
            except Exception as e:
                messages.error(request, "Error in adding the question "+str(e))
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'teacher/add_question.html', context)

        
# def manage_question(request):
#     questions = Question.objects.all()
#     context = {
#         'questions': questions,
#         'page_title': 'Manage Question'
#     }
#     return render(request, "teacher/manage_question.html", context)

def manage_question_class(request):
    teacher=get_object_or_404(Teacher,admin=request.user)
    level= Level.objects.filter(assignteacher__teacher=teacher).distinct()
    context = {
        'level':level,
        'page_title': 'Questions'
    }
    return render(request, "teacher/manage_question_class.html", context)


def manage_question(request,level_id):
    teacher=get_object_or_404(Teacher,admin=request.user)
    subject= Subject.objects.filter(level=level_id,assignteacher__teacher=teacher)
    level= Level.objects.get(id=level_id)
    context = {
        'subject':subject,
        'page_title': 'Select Subject to Add Questions for {0}'.format(level.level)
    }
    return render(request, "teacher/manage_question.html", context)

def view_question(request,subject_id):
    question=Question.objects.filter(subject=subject_id)
    subject = Subject.objects.get(id=subject_id)
    
    query = request.GET.get('q')
    if query:
        question = question.filter(Q(question__icontains=query) |
                                             Q(ans__icontains=query)).distinct()
        if not question:
            return render(request, "student/not_found.html")
    
    selected_status = request.GET.get('status')
    if selected_status:
        if selected_status == 'easy':
            question = question.filter(select_level='Easy')
        elif selected_status == 'difficult':
            question = question.filter(select_level='Difficult')
        
    
    
    context = {
        'question': question,
        'subject_id':subject_id,
        'page_title': '{0} Question'.format(subject.subject_name)
    }
    return render(request, "teacher/add_view_questions.html", context)


def edit_question(request, question_id):
    instance = get_object_or_404(Question, id=question_id)
    form = QuestionForm(request.POST or None, instance=instance)
    context = {
    'form': form,
    'question_id': question_id,
    'page_title': 'Edit Question'
    }
    if request.method == 'POST':
        if form.is_valid():
            questions = form.cleaned_data.get('question')
            select_level=form.cleaned_data.get('select_level')
            opt1=form.cleaned_data.get('op1')
            opt2=form.cleaned_data.get('op2')
            opt3=form.cleaned_data.get('op3')
            opt4=form.cleaned_data.get('op4')
            ans=form.cleaned_data.get('ans')
            try:
                # question.subject=subject
                question =Question.objects.get(id=question_id)
                # question.subject=subject
                question.select_level=select_level
                question.question=questions
                question.op1=opt1
                question.op2=opt2
                question.op3=opt3
                question.op4=opt4
                question.ans=ans 
                question.save()
                messages.success(request, "Successfully Edited")
                return redirect(reverse('view_questions', args=[question.subject.id]))
            except Exception as e:
                messages.error(request, "Could Not update " + str(e))
        else:
            messages.error(request, "Error in editing the question " +str(e))
    return render(request, 'teacher/edit_question.html', context)

def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        question.delete()
        messages.success(request, "The question has been deleted successfully!")
    except Exception:
        messages.error(
            request, "The question couldn't be deleted !! ")
    return redirect(reverse('view_questions', args=[question.subject.id]))



def add_notes(request,subject_id):
    form=NoteForm(request.POST or None, request.FILES or None)
    context = {
        'form': form,
        'page_title': 'Add Notes'
    }
    if request.method == 'POST':
        if form.is_valid():
            subject=subject_id
            title = form.cleaned_data.get('title')
            description=form.cleaned_data.get('description')
            images=request.FILES.get('images')
            file=request.FILES.get('file')
            try:
                note =Notes()
                s=Subject(pk=subject_id)
                # session=Session(pk=session_id)
                note.subject=s
                # note.subject=session
                note.title=title
                note.description=description
                note.images=images
                note.file=file
                # for image in images:
                #     note.images.create(image=image)
                # for file in file:
                #     note.file.create(file=file)
                note.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('manage_notes'))
            except Exception as e:
                messages.error(request, "Error in adding the notes "+str(e))
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'teacher/add_notes.html', context)


def manage_notes_batch(request):
    session=Session.objects.all()
    context = {
        'session':session,
        'page_title': 'Batch'
    }
    return render(request, "teacher/manage_notes_session.html", context)

def manage_notes_class(request,session_id):
    teacher=get_object_or_404(Teacher,admin=request.user)
    level= Level.objects.filter(assignteacher__teacher=teacher).distinct()
    context = {
        'level':level,
        'page_title': 'Notes',
        'session_id':session_id
    }
    return render(request, "teacher/manage_notes_class.html", context)


def manage_notes(request,session_id,level_id):
    teacher=get_object_or_404(Teacher,admin=request.user)
    subject= Subject.objects.filter(level=level_id,assignteacher__teacher=teacher)
    level= Level.objects.get(id=level_id)
    context = {
        'subject':subject,
        'page_title': 'Select Subject to Add/View Notes for {0}'.format(level.level),
        'session_id':session_id,
    }
    return render(request, "teacher/manage_notes.html", context)

def view_notes(request,session_id,level_id,subject_id):
    note=Notes.objects.filter(subject=subject_id).order_by('-updated_date')
    subject = Subject.objects.get(id=subject_id)
    context = {
        'note': note,
        'subject_id':subject_id,
        'page_title': '{0} Note'.format(subject.subject_name),
        'session_id':session_id,
        'level_id':level_id
    }
    return render(request, "teacher/view_notes.html", context)


# def view_aa(request):
#     student= get_object_or_404(Student, admin=request.user)
#     note = Notes.objects.all()
#     # subject=Subject.objects.all()
#     subject=Subject.objects.filter(level__student=student)
#     level = Level.objects.filter(student=student)
#     # subject=Subject.objects.filter(level=level).select_related('level')
#     context = {
#         'note': note,
#         'level':level,
#         'subject':subject,
#         'page_title': 'Manage Note'
#     }

#     return render(request, "student/student_view_notes.html", context)


def apply_leave(request):
    form = LeaveForm(request.POST or None)
    teacher = get_object_or_404(Teacher, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': Leave.objects.filter(teacher=teacher),
        'page_title': 'Apply for Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.teacher = teacher   
                obj.save()
                email_to = "aasishdeuja@gmail.com"
                email_from = "aasishdeuja@gmail.com"
                email_subject = "Leave Application - {0}".format(teacher)
                email_body = "Dear Administrator,\n\nI am writing to inform you that I have submitted a leave application. The details of my leave application are as follows:\n\nStart Date: {0}\nEnd Date: {1}\nReason for Leave: {2}\n\nThank you for your attention to this matter.\n\nSincerely,\n{3}".format(obj.start_date, obj.end_date, obj.reason, teacher)

                try:
                    send_mail(email_subject, email_body, email_from, [email_to], fail_silently=False)
                    messages.success(request, "Application for leave has been submitted for approval and an email has been sent to the administrator.")
                    return redirect(reverse('teacher_view_leave'))
                except Exception:
                    messages.error(request, "Could not send email to school administrator.")

                    return redirect(reverse('teacher_view_leave'))
            except Exception as e:
                messages.error(request, "Could not apply! " +str(e))
        else:
            messages.error(request, "Form has errors!")
    return render(request, "teacher/add_leave.html", context)

def teacher_view_leave(request):
    teacher = get_object_or_404(Teacher, admin_id=request.user.id)
    leave_history= Leave.objects.filter(teacher=teacher)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
        
    if start_date and end_date:
            leave_history = leave_history.filter(start_date__range=[start_date, end_date])
            
            if not leave_history:
                return render(request, "student/not_found.html")
    
    query = request.GET.get('q')
    if query:
        leave_history = leave_history.filter(Q(reason__icontains=query) |
                                             Q(start_date__icontains=query) |
                                             Q(end_date__icontains=query)).distinct()
        if not leave_history:
            return render(request, "student/not_found.html")
    
    selected_status = request.GET.get('status')
    
    if selected_status:
        if selected_status == 'pending':
            leave_history =  leave_history.filter(status=0)
        elif selected_status == 'approved':
            leave_history = leave_history.filter(status=1)
        elif selected_status == 'rejected':
            leave_history =  leave_history.filter(status=-1)
            
    context = {
       
        'leave_history': leave_history,
        'page_title': 'Apply for Leave'
    }
    return render(request, "teacher/apply_leave.html", context)

def manage_attendance_class(request):
    teacher = get_object_or_404(Teacher, admin=request.user)
    level= Level.objects.filter(assignteacher__teacher=teacher).distinct()
    context = {
        'level':level,
        'page_title': 'Attendance'
    }
    return render(request, "teacher/manage_attendance_class.html", context)

def manage_attendance(request,level_id):
    section = Section.objects.filter(level=level_id)
    level=Level.objects.get(id=level_id)
    context = {
        'section':section,
        'page_title': 'Attendance of {0}'.format(level)
    }
    return render(request, "teacher/manage_attendance.html", context)
    


def view_students_attendance(request,section_id):
    student= Student.objects.all()
    # students = Student.objects.filter(section=section_id)
    section=Student.objects.filter(section=section_id)


    context = {
        'section':section,
        'page_title': 'Manage Attendance'
    }

    return render(request, "teacher/students.html", context)



# def view_attendance(request,section_id):
#     students = Student.objects.filter(section=section_id)
#     # attendance = Attendance1.objects.all()
#     dates = Attendance1.objects.values_list('date', flat=True).distinct().order_by('date')
#     context = {
#         'students': students,
#         # 'attendance': attendance,
#         'dates': dates,
#         'page_title': 'Attendance'
#     }
    
#     return render(request, "attendance/view_attendance.html", context)


def view_attendance(request,section_id):
    students = Student.objects.filter(section=section_id)
    attendance = Attendance.objects.all().order_by('-date')
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
        # 'attendance':attendance,
        'attendance_by_month_paginated': attendance_by_month_paginated,
        'page_title': 'Attendance of {0} Section {1}'.format(section.level,section)
    }
    
    return render(request, "attendance/view_attendance.html", context)


# def view_attendance(request, section_id, month=None, year=None):
#     students = Student.objects.filter(section=section_id)
#     attendance = Attendance1.objects.all()
#     dates = Attendance1.objects.values_list('date', flat=True).distinct().order_by('date')
#     filtered_dates = [date for date in dates if date.month == month and date.year == year]
    
#     context = {
#         'students': students,
#         'attendance': attendance,
#         'dates': filtered_dates,
#         'page_title': 'Attendance'
#     }
    
#     return render(request, "attendance/view_attendance.html", context)



# def create_attendance(request):
#     if request.method == 'POST':
#         date = request.POST['date']
#         student_id = request.POST['student']
#         present = request.POST['present'] == 'on'
        
#         student = Student.objects.get(id=student_id)
#         attendance = Attendance1(date=date, student=student, present=present)
#         attendance.save()
        
#         return redirect('view_attendance')
        
#     students = Student.objects.all()
    
#     context = {
#         'students': students,
#         'page_title': 'Create Attendance'
#     }
    
#     return render(request, "attendance/create_attendance.html", context)

# def create_attendance(request):
#     if request.method == 'POST':
#         date = request.POST['date']
#         student_ids = request.POST.getlist('student')
#         presents = request.POST.getlist('present')

#         for i, student_id in enumerate(student_ids):
#             student = Student.objects.get(id=student_id)
#             present = presents[i] == 'on' if presents else False
#             attendance = Attendance1(date=date, student=student, present=present)
#             attendance.save()
        
#         return redirect('view_attendance')
        
#     students = Student.objects.all()
    
#     context = {
#         'students': students,
#         'page_title': 'Create Attendance'
#     }
    
#     return render(request, "attendance/create_attendance.html", context)


def create_attendance(request,section_id):
    if request.method == 'POST':
        date = request.POST['date']
        students = Student.objects.filter(section=section_id)
        section = Section.objects.get(id=section_id)
        
        if Attendance.objects.filter(date=date,section=section_id).exists():
            messages.error(request, 'Attendance for this date has already been recorded')
            return redirect('create_attendance',section_id=section_id)
        for student in students:
            student_id = student.id
            present = request.POST.get(str(student_id), False) == 'on'
            attendance = Attendance(date=date, student=student, section=section, present=present)
            attendance.save()
        messages.success(request, 'Attendance for this date has been added successfully.')
        return redirect('view_attendance',section_id)
        
    students = Student.objects.filter(section=section_id)
    section = Section.objects.get(id=section_id)
    context = {
        'students': students,
        # 'section_id':section_id,
        'page_title': 'Create Attendance of {0} Section {1}'.format(section.level,section)
    }
    
    return render(request, "attendance/create_attendance.html", context)




# def edit_attendance(request,section_id, attendance_id):
#     attendance = Attendance.objects.get(id=attendance_id)
#     if request.method == 'POST':
#         date = request.POST['date']
#         students = Student.objects.filter(section=section_id)
#         section = Section.objects.get(id=section_id)
#         # if Attendance.objects.filter(date=date,section=section_id).exclude(id=attendance_id).exists():
#         #     messages.error(request, 'Attendance for this date has already been recorded')
#         #     return redirect('edit_attendance',section_id=section_id, attendance_id=attendance_id)
#         for student in students:
#             student_id = student.id
#             present = request.POST.get(str(student_id), False) == 'on'
#             attendance.date = date
#             attendance.student = student
#             attendance.section = section
#             attendance.present = present
#             attendance.save()
            
#         messages.error(request, 'Attendance for this date has been updated successfully.')
#         return redirect('manage_attendance')
    
#     students = Student.objects.filter(section=section_id)

#     context = {
#         'attendance': attendance,
#         'students': students,
#         # 'section_id':section_id,
#         'page_title': 'Edit Attendance'
#     }

#     return render(request, "attendance/edit_attendance.html", context)


def edit_attendance(request,section_id):
    date = request.GET.get('date')
    attendance_list = Attendance.objects.filter(date=date,section=section_id)
    section = Section.objects.get(id=section_id)
    
    try:
        
        if request.method == 'POST':
            # Loop through all the attendance records for this date and update the present status
            for attendance in attendance_list:
                present = request.POST.get(str(attendance.student.id))
                if present == 'on':
                    attendance.present = True
                else:
                    attendance.present = False
                attendance.save()
                
            messages.success(request, 'Attendance for this date has been updated successfully.')
            return redirect('view_attendance',section_id)   
    except Exception:
        messages.error(request, 'Error in updating the attendance !!')
        return redirect('view_attendance',section_id) 
        
    context={
        'date': date, 
        'section_id':section_id,
        'attendance_list': attendance_list,
        'page_title': 'Edit Attendance of {0} Section {1}'.format(section.level,section)
        }
         
    return render(request, 'attendance/edit_attendance.html', context)


def teacher_download_all_attendance(request,section_id):
    students = Student.objects.filter(section=section_id)
    attendance = Attendance.objects.all().order_by('-date')
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
