from django.test import TestCase,RequestFactory
from .models import *
from knox.models import AuthToken
from django.urls import reverse
from rest_framework.test import APIClient
from .api import *
from rest_framework.test import force_authenticate
from django.test import Client


class test_Signup(TestCase):
    def test_user_post(self):
        response = self.client.post(reverse('RegistrationApi'),data={'first_name':'harsh','last_name':'kalal', 'email':'harshkalal2125@gmail.com','date_of_birth':'1997-11-11','password':'Hsbfk@1997','confirm_password':'Hsbfk@1997'})
        self.assertEqual(response.status_code, 201)
        
    def test_user_get(self):
        response = self.client.get('/api/register/')
        self.assertEqual(response.status_code, 200)

class test_project(TestCase):
    
    def setUp(self):
        self.api_client = APIClient()
        self.user = Signup.objects.create(first_name='harsh', last_name='kalal', email='harshkalal1997@gmail.com',date_of_birth='1997-11-11',password='Hsbfk@1997')                
        self.token = AuthToken.objects.create(user=self.user)

    def test_project_post(self):
        self.api_client.force_authenticate(self.user,self.token)
        response = self.api_client.post(reverse('ProjectApi'),{'name':'demo','signup':self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_project_get(self):
        self.api_client.force_authenticate(self.user,self.token)
        response = self.api_client.get(reverse('ProjectApi'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class test_review(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.user = Signup.objects.create(first_name='harsh', last_name='kalal', email='harshkalal1997@gmail.com',date_of_birth='1997-11-11',password='Hsbfk@1997')                
        self.token = AuthToken.objects.create(user=self.user)
        self.project = Project.objects.create(name = 'demo2', signup = self.user)

    def test_review_post(self):
        self.api_client.force_authenticate(self.user,self.token)
        response = self.api_client.post(reverse('ReviewApi'),{'name':'Reviewname1','project':self.project.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
    def test_review_get(self):
        self.api_client.force_authenticate(self.user,self.token)
        response = self.api_client.get(reverse('ReviewApi'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class test_login(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.user = Signup.objects.create(first_name='harsh', last_name='patel', email='harshkalal2125@gmail.com',date_of_birth='1997-11-11',password='Kalal@1997')                
        # self.token = AuthToken.objects.create(user=self.user)

    def test_valid_post(self):
        self.api_client.force_login(self.user)
        response = self.api_client.post(reverse('knox_login'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
    