from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile

# class TestLogin(TestCase):
    # def setUp(self):
    #     self.client = Client()
    #     self.login_url = reverse('user_login')
    #     self.loginurl = reverse('loginpage')
    #     self.admin_home_page_url = reverse('admin_home_page')
    #     self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')

    # def test_login_with_valid_credentials(self):
    #     response = self.client.post(self.login_url, {
        # 'email': 'hamrotuition@gmail.com', 
        # 'password': '12345678'
        # })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, self.admin_home_page_url)

#     def test_login_invalid_credentials(self):
#         response = self.client.post(self.login_url, {
#             'email': 'hamrotuition@gmail.com',
#             'password': 'wrongpassword'
#         })
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.loginurl)
        
#     def test_login_with_no_data(self):
#         response = self.client.post(self.loginurl, {})
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'login/login1.html')





# class LevelTestCase(TestCase):

#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.url=reverse('add_class')
        
#     def test_add_level_successful(self):
#         data = {'level': 'Class 10'}
#         response = self.client.post(self.url, data=data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.url)
    
    # def test_add_level_invalid_data(self):
    #     data = {'level': ''}
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Could Not Add')




# class EditClassTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.level = Level.objects.create(level="Class 8")
#         self.url = reverse('edit_class', args=[self.level.id])
#         self.return_url = reverse('manage_class')

#     def test_edit_level_successful(self):
#         data = {'level': 'Class 9'}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.return_url)
#         self.assertEqual(Level.objects.get(id=self.level.id).level, 'Class 9')


#     def test_edit_level_invalid_data(self):
#         data = {'level': ''}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Could Not Update')
        
        
    
    



# class DeleteLevelTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.level = Level.objects.create(level='Class 10')

#     def test_delete_level_successful(self):
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         response = self.client.delete(reverse('delete_class', args=[self.level.id]))
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(Level.objects.filter(id=self.level.id).exists())





# class AddSessionTestCase(TestCase):

#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.url=reverse('add_session')
        
#     def test_add_session_successful(self):
#         data = {'year': 2017}
#         response = self.client.post(self.url, data=data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.url)  
    
#     def test_add_session_invalid_data(self):
#         data = {'year': ''}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'This field is required.')
#         self.assertEqual(Session.objects.count(), 0)



# class EditSessionTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.session = Session.objects.create(year=2023)
#         self.url = reverse('edit_session', args=[self.session.id])
        
#     def test_edit_session_sucessful(self):
#         data = {'year': 2024}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.url)
#         self.assertEqual(Session.objects.get(id=self.session.id).year, 2024)


#     def test_edit_session_invalid_data(self):
#         data = {'year': ''}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Invalid Form Submitted')
        
    
    
# class DeleteSessionTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.session = Session.objects.create(year=2018)

#     def test_delete_session_successful(self):
#         response = self.client.delete(reverse('delete_session', args=[self.session.id]))
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(Session.objects.filter(id=self.session.id).exists())



# class AddSectionTestCases(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.url=reverse('add_section')
#         self.level=Level.objects.create(level='Class 10')
        
    # def test_add_section_successful(self):
    #     data = {
    #             'section':'A',
    #             'level':self.level.id
    #         }
    #     response = self.client.post(self.url, data=data)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, self.url)  
        
        
    # def test_add_section_invalid_data(self):
    #     data = {
    #             'section':'',
    #             'level':self.level.id
    #         }
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'This field is required.')
    #     self.assertEqual(Section.objects.count(), 0)
    
    
# class EditSectionTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.level=Level.objects.create(level='Class 10')
#         self.section = Section.objects.create(section='A',level=self.level)
#         self.url = reverse('edit_section', args=[self.section.id])
#         self.return_url = reverse('manage_section')
        
#     def test_edit_section_sucessful(self):
#         data = {
#                 'section':'B',
#                 'level':self.level.id
#             }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.return_url)
#         self.assertEqual(Section.objects.get(id=self.section.id).section, 'B')

#     def test_edit_section_invalid_data(self):
#         data = {
#                 'section':'',
#                 'level':self.level.id
#             }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'This field is required.')


# class DeleteSectionTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.level=Level.objects.create(level='Class 10')
#         self.section = Section.objects.create(section='A',level=self.level)

#     def test_delete_section_successful(self):
#         response = self.client.delete(reverse('delete_section', args=[self.section.id]))
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(Section.objects.filter(id=self.section.id).exists())



# class AddSubjectTestCases(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.url=reverse('add_subject')
#         self.level=Level.objects.create(level='Class 10')
        
#     def test_add_subject_successful(self):
#         data = {
#                 'code':'CA11',
#                 'subject_name':'Computer',
#                 'marks':100,
#                 'level':self.level.id
#             }
#         response = self.client.post(self.url, data=data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.url)  
        
        
#     def test_add_subject_invalid_data(self):
#         data = {
#                 'code':'',
#                 'subject_name':'',
#                 'marks':100,
#                 'level':self.level.id
#             }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'This field is required.')
#         self.assertEqual(Subject.objects.count(), 0)
    
    
# class EditSubjectTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.level=Level.objects.create(level='Class 10')
#         self.subject = Subject.objects.create(code='C11',subject_name='Computer',marks=100,level=self.level)
#         self.url = reverse('edit_subject', args=[self.subject.id])
#         self.return_url = reverse('manage_subject')
        
#     def test_edit_subject_sucessful(self):
#         data = {
#                 'code':'EN12',
#                 'subject_name':'English',
#                 'marks':100,
#                 'level':self.level.id
#             }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.url)
#         self.assertEqual(Subject.objects.get(id=self.subject.id).subject_name, 'English')

#     def test_edit_subject_invalid_data(self):
#         data = {
#                 'code':'',
#                 'subject_name':'',
#                 'marks':100,
#                 'level':self.level.id
#             }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'This field is required.')


# class DeleteSubjectTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.level=Level.objects.create(level='Class 10')
#         self.subject = Subject.objects.create(code='C11',subject_name='Computer',marks=100,level=self.level)

#     def test_delete_subject_successful(self):
#         response = self.client.delete(reverse('delete_subject', args=[self.subject.id]))
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(Subject.objects.filter(id=self.subject.id).exists())


#Book Test

# class AddBookTestCases(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.url=reverse('add_book')
#         self.return_url=reverse('manage_book')
        
#     def test_add_book_successful(self):
#         data = {
#             'title': 'Django for Beginers',
#             'author': 'Ashish Deuja',
#             'year': '2022',
#             'publisher': 'A.B Publications',
#             'desc': 'Best Book for Beginers',
#             'pdf': SimpleUploadedFile("bookapp/pdfs/file.pdf", b"file_content",content_type="application/pdf"),
#             'cover': SimpleUploadedFile("bookapp/covers/file.jpg", b"file_content",content_type="image/jpeg"),
#         }
#         response = self.client.post(self.url, data=data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.return_url)  
        
        
#     def test_add_subject_invalid_data(self):
#         data = {
#             'title': 'Django for Beginers',
#             'author': 'Ashish Deuja',
#             'year': '2022',
#             'publisher': 'A.B Publications',
#             'desc': '',
#             'pdf': '',
#             'cover': '',
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'This field is required.')
#         self.assertEqual(Book.objects.count(), 0)
    
    
# class EditBookTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.url=reverse('edit_book')
#         self.return_url=reverse('manage_book')
        
#     def test_edit_book_sucessful(self):
#         data = {
#                 'code':'EN12',
#                 'subject_name':'English',
#                 'marks':100,
#                 'level':self.level.id
#             }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, self.url)
#         self.assertEqual(Subject.objects.get(id=self.subject.id).subject_name, 'English')

#     def test_edit_book_invalid_data(self):
#         data = {
#                 'code':'',
#                 'subject_name':'',
#                 'marks':100,
#                 'level':self.level.id
#             }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'This field is required.')


# class DeleteSubjectTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(email='hamrotuition@gmail.com', password='12345678', user_type='1')
#         self.client.login(email='hamrotuition@gmail.com', password='12345678')
#         self.level=Level.objects.create(level='Class 10')
#         self.subject = Subject.objects.create(code='C11',subject_name='Computer',marks=100,level=self.level)

#     def test_delete_subject_successful(self):
#         response = self.client.delete(reverse('delete_subject', args=[self.subject.id]))
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(Subject.objects.filter(id=self.subject.id).exists())


          


