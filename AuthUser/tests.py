import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from .models import AuthUser
from .views import AuthUserRegisterView
from rest_framework.authtoken.models import Token
# Create your tests here.
# https://realpython.com/test-driven-development-of-a-django-restful-api/ follow this article for how we write test case
class AuthUserTestModel(TestCase):
    def setUp(self):
        AuthUser.objects.create( email='rohansingh9211@gmail.com', name='rohan',tc=False,is_active=True,is_admin=False)
        AuthUser.objects.create( email='ramjana321@gmail.com', name='ram',tc=True,is_active=True,is_admin=False)

    def test_AuthUser_get(self):
        authuserrohan = AuthUser.objects.get(name='rohan')
        authuserram = AuthUser.objects.get(name='ram')
        self.assertEqual(authuserrohan.name,'rohan')
        self.assertEqual(authuserram.name,'ram')

class AuthRegisterTest(TestCase):
    def setUp(self):
        self.registerUserRohan={
            "email":"rohansingh@gmail.com",
            "name":"rohan",
            "password":"Rohan@12345",
            "password2":"Rohan@12345",
            "tc":"true"
        }
        self.registerUserRam={
            "email":"rambilas@gmail.com",
            "name":"ram",
            "password":"ram@12345",
            "password2":"ram@12345",
            "tc":"false"
        }
        
    def test_register_post(self):
        response=self.client.post(
            reverse('register'),
            data=json.dumps(self.registerUserRam),
            content_type='application/json',
        )
        self.assertEqual(self.registerUserRam['password'],self.registerUserRam['password2'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class AuthUserChangePassword(TestCase):
    print('hello')
    def setUp(self):
        self.user = AuthUser.objects.create(email='rohansingh9211@gmail.com', password="rohan0123456", name='rohan', tc=False, is_active=True, is_admin=False)
        

    def test_change_password(self):
        print(f"User: {self.user.email}, Password: {self.user.password}")
        
        logged_in = self.client.login(email="rohansingh9211@gmail.com", password="rohan0123456")
        print("Logged in:", logged_in)
    

        self.rohanChange = {
            "password": "rohan@123",
            "password2": "rohan@123",
        }

        response = self.client.post(
            reverse('change password'),
            data=json.dumps(self.rohanChange),
            content_type='application/json',
        )
        
        print("Response status:", response.status_code)
        print("Response content:", response.content)
        
        self.assertEqual(self.rohanChange['password'], self.rohanChange['password2'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
