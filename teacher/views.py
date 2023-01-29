from django.shortcuts import render,get_object_or_404,redirect,reverse
from .forms import *
from django.core.mail import send_mail
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


def manage_question(request):
    subject= Subject.objects.all()
    context = {
        'subject':subject,
        'page_title': 'Questions'
    }
    return render(request, "teacher/manage_question.html", context)

def view_question(request,subject_id):
    question=Question.objects.filter(subject=subject_id)
    subject = Subject.objects.get(id=subject_id)
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
                note.subject=s
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

def manage_notes(request):
    note = Notes.objects.all()
    level = Subject.objects.all()
    teacher=Teacher.objects.all()
    context = {
        'note': note,
        'level':level,
        'teacher':teacher,
        'page_title': 'Notes'
    }
    return render(request, "teacher/manage_notes.html", context)

def view_notes(request,subject_id):
    note=Notes.objects.filter(subject=subject_id).order_by('-updated_date')
    subject = Subject.objects.get(id=subject_id)
    context = {
        'note': note,
        'subject_id':subject_id,
        'page_title': '{0} Note'.format(subject.subject_name)
    }
    return render(request, "teacher/view_notes.html", context)


def view_aa(request):
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

    return render(request, "teacher/aa_notes.html", context)


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
                # email = request.user.email      
                obj.save()
                email_to = "aasishdeuja@gmail.com"
                # email_to = "dipinbhandari101@gmail.com "
                email_from = "aasishdeuja@gmail.com"
                email_subject = "Leave Application - {0}".format(teacher)
                email_body = "Dear Administrator,\n\nI am writing to inform you that I have submitted a leave application. The details of my leave application are as follows:\n\nStart Date: {0}\nEnd Date: {1}\nReason for Leave: {2}\n\nThank you for your attention to this matter.\n\nSincerely,\n{3}".format(obj.start_date, obj.end_date, obj.reason, teacher)

                try:
                    send_mail(email_subject, email_body, email_from, [email_to], fail_silently=False)
                    messages.success(request, "Application for leave has been submitted for approval and an email has been sent to the administrator.")
                except Exception:
                    messages.error(request, "Could not send email to school administrator.")

                    return redirect(reverse('apply_leave'))
            except Exception as e:
                messages.error(request, "Could not apply! " +str(e))
        else:
            messages.error(request, "Form has errors!")
    return render(request, "teacher/apply_leave.html", context)




def bookmarked_book(request):
    teacher = get_object_or_404(Teacher, admin_id=request.user.id)
    context = {
        'bookmarks': Bookmark.objects.filter(teacher=teacher).order_by('-updated_at'),
        'page_title': 'Books'
    }
    return render(request, "book/bookmark.html", context)

def create_bookmark(request, book_id): 
    teacher = get_object_or_404(Teacher, admin=request.user)
    book = get_object_or_404(Book, pk=book_id)
    existing_bookmark = Bookmark.objects.filter(teacher=teacher, book=book).first()
    try:
        if existing_bookmark:
            messages.info(request, "This book is already bookmarked.")
            return redirect(reverse('bookmark_book'))
        else:
            Bookmark.objects.create(teacher=teacher, book=book)
            messages.success(request, "The book has been bookmarked successfully.")
            return redirect(reverse('bookmark_book'))
    except Exception as e:
        messages.error(request, "An error occurred while bookmarking the book.")
        return redirect(reverse('bookmark_book'))

def delete_bookmark(request, bookmark_id):
    teacher = get_object_or_404(Teacher, admin_id=request.user.id)
    bookmark = get_object_or_404(Bookmark, pk=bookmark_id, teacher=teacher)
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