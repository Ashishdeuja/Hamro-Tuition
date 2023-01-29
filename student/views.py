import random
from django.shortcuts import render,get_object_or_404,redirect,reverse

from teacher.models import *
from .forms import *
from django.core.mail import send_mail
from administratior.forms import *
from administratior.models import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


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

                random_questions = random.sample(list(question), 1)
                
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

