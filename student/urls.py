from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.student_home_page, name='student_home_page'),
    path("student/profile/", views.student_profile, name='student_profile'),
    path('view/notes',views.view_notes,name='view_notes'),
    path('subject/view/notes/<int:session_id>/<int:subject_id>',views.view_subject_notes,name='subject_view_notes'),
    path('view/question',views.view_question,name='student_view_question'),
    path('level/selection/<int:session_id>/<int:subject_id>',views.test_level_selection,name='test_level_selection'),
    path('start/test/<int:session_id>/<int:subject_id>/',views.start_test,name='start_test'),
    path('test/question/<int:session_id>/<int:subject_id>/', views.test_home, name='test_question'),
    path('test/result/pdf/<int:test_id>/',views.mock_test_result_pdf,name='mock_test_result_pdf'),
    path('bookmarked/books/',views.bookmarked_book,name='bookmark_book'),
    path('create/bookmark/<int:book_id>/',views.create_bookmark, name='create_bookmark'),
    path('delete/bookmark/<int:bookmark_id>/', views.delete_bookmark, name='delete_bookmark'),
    path("apply/leave/", views.student_apply_leave,name='student_apply_leave'),
    path("view/leave/", views.student_view_leave,name='student_view_leave'),
    path('add/testimonial/', views.add_testimonial, name='add_testimonial'),
    path('manage/testimonial/', views.manage_testimonial, name='manage_testimonial'),
    path('display/attendance/',views.student_view_attendance,name='student_view_attendance'),
    path('view/attendance/pdf',views.student_attendance_pdf,name='student_attendance_pdf'),
    path('view/daily/attendance/pdf',views.daily_attendance_pdf,name='daily_attendance_pdf'),
    path('view/weekly/attendance/pdf',views.weekly_attendance_pdf,name='weekly_attendance_pdf'),
    path('view/yearly/attendance/pdf',views.yearly_attendance_pdf,name='yearly_attendance_pdf'),
    path("khalti/",views.khaltipayment,name='khalti_int'),
    path("payment/success/",views.successPayment,name='success'),
    
]