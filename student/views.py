from http.client import HTTPResponse
import random
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.http import HttpResponse, FileResponse
from teacher.forms import LeaveForm
from .models import *
from teacher.models import *
from .forms import *
from django.core.mail import send_mail
from administratior.forms import *
from administratior.models import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.loader import get_template
from xhtml2pdf import pisa

# from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import weasyprint




def view_notes(request):
    student= get_object_or_404(Student, admin=request.user)
    note = Notes.objects.all()
    # subject=Subject.objects.all()
    subject=Subject.objects.filter(level__student=student)
    level = Level.objects.filter(student=student)
    # subject=Subject.objects.filter(level=level).select_related('level')
    context = {
        'note': note,
        'level':level,
        'subject':subject,
        'page_title': 'Manage Note'
    }

    return render(request, "student/student_view_notes.html", context)

def view_subject_notes(request,subject_id):
    note=Notes.objects.filter(subject=subject_id).order_by('-updated_date')
    subject = Subject.objects.get(id=subject_id)
    context = {
        'note': note,
        'subject_id':subject_id,
        'page_title': '{0} Note'.format(subject.subject_name)
    }
    return render(request, "student/subject_view_notes.html", context)


def view_question(request):
    student= get_object_or_404(Student, admin=request.user)
    question = Question.objects.all()
    subject=Subject.objects.filter(level__student=student)
    level = Level.objects.filter(student=student)
    context = {
        'note': question,
        'level':level,
        'subject':subject,
        'page_title': 'Question'
    }

    return render(request, "student/view_question.html", context)

def test_level_selection(request,subject_id):
    # if request.method == 'POST':
        # selected_level= request.POST.get('selected_level')
        questions = Question.objects.filter(subject=subject_id)
        context = {
            'questions': questions,
            'subject_id':subject_id
                   }
        return render(request, 'student/start_test.html', context)

# @csrf_exempt
def test_home(request,subject_id):
    # subject=Subject.objects.filter(id=subject_id)
    if request.method == 'POST':
        try:
            questions = Question.objects.filter(subject=subject_id)
            q={}
            for key,value in request.POST.items():
                if '__answer' in key:
                    q[key.replace('__answer','')]=value
            print(q)
            
            _actual_questions=Question.objects.filter(id__in = q.keys())
            print(_actual_questions)
            score = 0
            total=0
            
            for question in _actual_questions:
                if question.ans == q[str(question.id)]:
                    score+=10
                    total+=1
            
            print(score)
            print(request.POST.keys())
            context = {
                'questions': questions, 
                'score': score,
                'total':len(_actual_questions),
                'correct':total,
                'incorrect':len(_actual_questions)-total,
                'percentage':(total/len(_actual_questions))*100,
                'subject_id':subject_id,
                'student_name':request.user.first_name + ' '+ request.user.last_name, 
                'subject':question.subject.subject_name,
                'class': question.subject.level   
                }
            return render(request, 'student/result.html', context)
        except ValueError as e:
            messages.error(request, "The number of questions available is insufficient to conduct the test."+str(e))
            return redirect('student_view_question')
    # else:
    #     try:
    #         question=Question.objects.filter(subject=subject_id)

    #         random_questions = random.sample(list(question), 2)
            
    #         context = {
    #             'question':question,
    #             'questions':random_questions
                
                    
    #         }
    #         return render(request,'student/test_home.html',context)
        
    #     except ValueError as e:
    #         messages.error(request, "The number of questions available is insufficient to conduct the test.")
    #         return redirect('student_view_question')
    
    
    # questions = Question.objects.filter(subject=subject_id)
    # return render(request,"student/test_home.html",{"questions":questions})
    
    
def start_test(request,subject_id):
    try:
                level = request.POST.get('select_level')
                if level == '':
                    messages.error(request, "Please select the level to start the test.")
                    return redirect('test_level_selection', subject_id)
                question=Question.objects.filter(subject=subject_id,select_level=level)

                random_questions = random.sample(list(question), 5)
                
                context = {
                    'question':question,
                    'questions':random_questions,
                    'subject_id':subject_id
                        
                }
                return render(request,'student/test_home.html',context)
        
    except ValueError as e:
        messages.error(request, "The number of questions available is insufficient to conduct the test.")
        return redirect('test_level_selection', subject_id)
    

# def mock_test_result_pdf(request, subject_id):
#     questions = Question.objects.filter(subject=subject_id)
#     q={}
#     for key,value in request.POST.items():
#         if '__answer' in key:
#             q[key.replace('__answer','')]=value
#     # print(q)
    
#     _actual_questions=Question.objects.filter(id__in = q.keys())
#     # print(_actual_questions)
#     score = 0
#     total=0
            
#     for question in _actual_questions:
#         if question.ans == q[str(question.id)]:
#             score+=10
#             total+=1
            
#     print(score)
#     print(request.POST.keys())
#     html = render_to_string('student/mock_test_result_pdf.html',{
#                 'questions': questions, 
#                 'score': score,
#                 'total':len(_actual_questions),
#                 'correct':total,
#                 'incorrect':len(_actual_questions)-total,
#                 'percentage':(total/len(_actual_questions))*100,
#                 'subject_id':subject_id
                
#                 }
#             )
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=result.pdf'
#     weasyprint.HTML(string=html).write_pdf(response,
#     stylesheets=[weasyprint.CSS(
#     settings.STATIC_ROOT + 'css/pdf.css')])
#     return response

def bookmarked_book(request):
    student = get_object_or_404(Student, admin_id=request.user.id)
    context = {
        'bookmarks': Bookmark.objects.filter(student=student).order_by('-updated_at'),
        'page_title': 'Books'
    }
    return render(request, "book/bookmark.html", context)

def create_bookmark(request, book_id): 
    student = get_object_or_404(Student, admin=request.user)
    book = get_object_or_404(Book, pk=book_id)
    existing_bookmark = Bookmark.objects.filter(student=student, book=book).first()
    try:
        if existing_bookmark:
            messages.info(request, "This book is already bookmarked.")
            return redirect(reverse('bookmark_book'))
        else:
            Bookmark.objects.create(student=student, book=book)
            messages.success(request, "The book has been bookmarked successfully.")
            return redirect(reverse('bookmark_book'))
    except Exception as e:
        messages.error(request, "An error occurred while bookmarking the book.")
        return redirect(reverse('bookmark_book'))

def delete_bookmark(request, bookmark_id):
    student = get_object_or_404(Student, admin_id=request.user.id)
    bookmark = get_object_or_404(Bookmark, pk=bookmark_id, student=student)
    try:
        bookmark.delete()
        messages.success(request, "Bookmark removed successfully.")
        return redirect(reverse('bookmark_book'))
    except Bookmark.DoesNotExist:
        messages.error(request, "This bookmark does not exist.")
        return redirect(reverse('bookmark_book'))
    except Exception as e:
        messages.error(request, "An error occurred while removing the bookmark.")
        return redirect(reverse('bookmark_book'))
    return redirect(reverse('bookmark_book'))



def student_apply_leave(request):
    form = LeaveForm(request.POST or None)
    student = get_object_or_404(Student, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': Leave.objects.filter(student=student),
        'page_title': 'Apply for Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.student = student
                # email = request.user.email      
                obj.save()
                email_to = "aasishdeuja@gmail.com"
                # email_to = "dipinbhandari101@gmail.com "
                email_from = "aasishdeuja@gmail.com"
                email_subject = "Leave Application - {0}".format(student)
                email_body = "Dear Administrator,\n\nI am writing to inform you that I have submitted a leave application. The details of my leave application are as follows:\n\nStart Date: {0}\nEnd Date: {1}\nReason for Leave: {2}\n\nThank you for your attention to this matter.\n\nSincerely,\n{3}".format(obj.start_date, obj.end_date, obj.reason, student)

                try:
                    send_mail(email_subject, email_body, email_from, [email_to], fail_silently=False)
                    messages.success(request, "Application for leave has been submitted for approval and an email has been sent to the administrator.")
                    return redirect(reverse('student_view_leave'))
                except Exception:
                    messages.error(request, "Could not send email to school administrator.")

                    return redirect(reverse('student_view_leave'))
            except Exception as e:
                messages.error(request, "Could not apply! " +str(e))
        else:
            messages.error(request, "Form has errors!")
    return render(request, "student/student_add_leave.html", context)

def student_view_leave(request):
    student = get_object_or_404(Student, admin_id=request.user.id)
    context = {
       
        'leave_history': Leave.objects.filter(student=student),
        'page_title': 'Apply for Leave'
    }
    return render(request, "student/student_apply_leave.html", context)



def add_testimonial(request):
    form = TestimonialForm(request.POST or None, request.FILES or None)
    student = get_object_or_404(Student, admin_id=request.user.id)
    context = {
        'form': form,
        'page_title': 'Add Testimonial'
    }
    if request.method == 'POST':
        if form.is_valid():
            image=request.FILES.get('image')
            description = form.cleaned_data.get('description')

            try:
                notice=Testimonial()
                notice.student=student
                notice.image=image
                notice.description=description
                notice.save()
                messages.success(request, ('Testimonial has been uploaded.'))
                return redirect('manage_testimonial')
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
                
        else:
            messages.error(request, 'Please correct the error(s) below.')
    return render(request, 'student/add_testimonial.html',context)


def manage_testimonial(request):
    student = get_object_or_404(Student, admin_id=request.user.id)
    testimonials=Testimonial.objects.filter(student=student)
    context = {
       
        'testimonials':testimonials ,
        'page_title': 'Testimonial'
    }
    return render(request, "student/manage_testimonial.html", context)
    # return render(request, "admin/index.html", context)


def student_view_attendance(request):
    student= get_object_or_404(Student, admin=request.user)
    attendance = Attendance.objects.filter(student=student).order_by('-date')
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
    
    # template = get_template("attendance/student_view_attendance.html")
    # html = template.render(context)
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="attendance.pdf"'
    # pisaStatus = pisa.CreatePDF(html, dest=response)

    # if pisaStatus.err:
    #     return HttpResponse("PDF creation error: {0}".format(pisaStatus.err))
    # else:
    #     return response
    return render(request, "attendance/student_view_attendance.html", context)