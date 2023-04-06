from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from unittest.mock import patch
from .models import *
from teacher.models import *
# Create your tests here.
# class AuthenticationTestCase(TestCase):
#     def setUp(self):
#         pass
    
    # def test_check_login_view(self):
    #     response = self.client.get('http://127.0.0.1:8000/login')
    #     self.assertEqual(response.status_code,200)


# class PaymentTestCase(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(email='ashish@gmail.com', password='12345678', user_type='3')
#         self.level = Level.objects.create(level="Class 10")
#         self.section = Section.objects.create(section="A",level=self.level)
#         self.session = Session.objects.create(year=2022)
#         self.student = Student.objects.create(
#             admin=self.user,
#             fathers_name="Krishna Deuja",
#             fathers_number="9812021023",
#             mothers_name="Manju",
#             mothers_number="9810124365",
#             level=self.level,
#             section=self.section,
#             session=self.session
#         )
#         self.client.login(email='ashish@gmail.com', password='12345678')
#         self.khalti_url = reverse('khalti_int')
#         self.success_url = reverse('success')
        

#     def test_authorization_failure(self):
#         url = 'https://a.khalti.com/api/v2/epayment/initiate/'
#         headers = {
#             'Authorization': 'Key invalid_key'
#         }
#         response = self.client.post(url, headers=headers)
#         self.assertEqual(response.status_code, 404)
        
#     def test_payment_invalid_amount(self):
#         data={
#             'amount':9
#         }
#         response= self.client.post(self.khalti_url, data)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.headers["Location"], '/student/khalti/')

#     def test_payment_successful(self):
#         amount = 20
#         with patch('requests.post') as mock_post:
#             mock_post.return_value.json.return_value = {
#                 'payment_url': self.success_url
#             }
#             response = self.client.post(self.khalti_url, {'amount': amount})
#             response = self.client.get(self.success_url + f'?message=&amount={amount * 100}')
#             payment = Payment.objects.create(student=self.student, amount=20)
#             self.assertEqual(response.status_code, 302)
#             self.assertEqual(mock_post.call_count, 1)
#             payment = Payment.objects.first()
#             self.assertEqual(payment.amount, amount)
            


# from django.test import TestCase, Client
# from django.urls import reverse
# from teacher.models import Question
# from .views import start_test

# class StartTestViewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.level=Level.objects.create(level="Class 10")
#         self.session_id = Session.objects.create(year=2023)
#         self.subject_id = Subject.objects.create(code="CA21",subject_name="Computer",marks=100,level=self.level)
#         self.level = 'easy'
#         self.question = Question.objects.create(
#             subject=self.subject_id,
#             select_level=self.level,
#             session=self.session_id,
#             question='What is the capital of Nepal?',
#             op1='Delhi',
#             op2='Kathmandu',
#             op3='Biratnagar',
#             op4='Dhaka',
#             ans='Kathmandu',
#         )

#     def test_valid_input(self):
#         url = reverse('start_test', args=[self.session_id.id, self.subject_id.id])
#         data={
#             'select_level': self.level
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)


