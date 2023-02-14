from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user 
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "administratior.views":
                    pass
                else:
                    return redirect(reverse("admin_home_page"))
            elif user.user_type == "2":
                if modulename == "teacher.views":
                    pass
                elif modulename == "administratior.views":
                    pass
                else:
                    return redirect(reverse("teacher_home_page"))
            elif user.user_type == "3":
                if modulename == "student.views":
                    pass
                elif modulename == "administratior.views":
                    pass
                else:
                    return redirect(reverse("student_home_page"))
            else:
                return redirect(reverse("loginpage"))
    
        else:
            if request.path == reverse('loginpage') or  request.path == reverse('user_login'): 
                pass
            else:
                return redirect(reverse('loginpage'))
