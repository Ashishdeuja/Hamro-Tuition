from django.urls import path
from . import views

urlpatterns = [
    path('view/question',views.view_question,name='student_view_question'),
    path('level/selection/<int:subject_id>',views.test_level_selection,name='test_level_selection'),
    path('start/test/<int:subject_id>/',views.start_test,name='start_test'),
    # path('test/question/<int:subject_id>',views.test_home,name='test_question'),
    path('test/question/<int:subject_id>/', views.test_home, name='test_question'),
    # path('test/result/pdf/<int:subject_id>/',views.mock_test_result_pdf,name='mock_test_result_pdf'),
]