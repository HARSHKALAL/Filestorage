from django.test import TestCase,RequestFactory
from .models import *
from knox.models import AuthToken
from django.urls import reverse
from rest_framework.test import APIClient

class test_Signup(TestCase):
    def test_user_post(self):
        response = self.client.post(reverse('RegistrationApi'),data={'first_name':'harsh','last_name':'kalal', 'email':'harshkalal2125@gmail.com','date_of_birth':'1997-11-11','password':'Hsbfk@1997','confirm_password':'Hsbfk@1997'})
        self.assertEqual(response.status_code, 201)
        
    def test_user_get(self):
        response = self.client.get('/api/register/')
        self.assertEqual(response.status_code, 200)

class test_project(TestCase):

    def setUp(self):
        self.client = APIClient()                
        self.user = Signup.objects.create(first_name='harsh', last_name='kalal', email='harshkalal1997@gmail.com',date_of_birth='1997-11-11',password='Hsbfk@1997')                
        self.token = AuthToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_project_get(self):
        response = self.client.get('/api/project/')
        self.assertEqual(response.status_code,200) 

