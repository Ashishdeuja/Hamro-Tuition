from django.urls import path
from . import views



urlpatterns = [
    path("home/page/", views.teacher_home_page, name='teacher_home_page'),
    path("profile/", views.teacher_profile, name='teacher_profile'),
    path('add/question/<int:session_id>/<int:subject_id>',views.add_question,name='add_question'),
    path('manage/question/session',views.manage_question_batch,name='manage_question_batch'),
    path('manage/question/<int:session_id>/class',views.manage_question_class,name='manage_question'),
    path('manage/question/<int:session_id>/<int:level_id>',views.manage_question,name='manage_question_subject'),
    
    path('view/questions/<int:session_id>/<int:level_id>/<int:subject_id>',views.view_question,name='view_questions'),
    path('add/notes/<int:session_id>/<int:subject_id>/',views.add_notes,name='add_notes'),
    path('manage/notes/<int:session_id>/class',views.manage_notes_class,name='manage_notes'),
    path('manage/notes/session',views.manage_notes_batch,name='manage_notes_batch'),
    path('manage/notes/<int:session_id>/<int:level_id>',views.manage_notes,name='manage_notes_subject'),
    path('edit/note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete/note/<int:note_id>/', views.delete_notes, name='delete_note'),
    
    
    path('view/notes/<int:session_id>/<int:level_id>/<int:subject_id>/',views.view_notes,name='view_notes'),
    path('edit/question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete/question/<int:question_id>/', views.delete_question, name='delete_question'),
    path("apply/leave/", views.apply_leave,name='apply_leave'),
    path("view/leave/", views.teacher_view_leave,name='teacher_view_leave'),
    path('manage/attendance/session',views.manage_attendance_batch,name='manage_attendance_batch'),
    path('manage/attendance/<int:session_id>/<int:level_id>',views.manage_attendance,name='manage_attendance'),
    path('student/attendance/view/<int:session_id>/<int:level_id>/<int:section_id>/',views.view_students_attendance,name='view_students_attendance'),
    path('manage/attendance/<int:session_id>/class',views.manage_attendance_class,name='manage_attendance_class'),
    path('view/attendance/<int:session_id>/<int:level_id>/<int:section_id>/',views.view_attendance,name='view_attendance'),
    path('create/attendance/<int:session_id>/<int:section_id>', views.create_attendance, name='create_attendance'),
    path('edit/attendance/<int:session_id>/<int:section_id>/', views.edit_attendance, name='edit_attendance'),
    path('download/all/attendance/<int:session_id>/<int:section_id>',views.teacher_download_all_attendance,name='teacher_download_all_attendance'),
    

   
]