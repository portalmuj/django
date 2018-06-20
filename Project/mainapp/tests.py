from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from captcha.fields import CaptchaField
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import OfferForm, UserForm, EmployerForm, OfferResponseForm
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your tests here.
from mainapp.models import Employer
from django.test import Client


class EmployerAddingTest(TestCase):
    def test(self):
        c = Client()
        us = User.objects.create(username="testUser", password="test", email="email", last_login=timezone.now(),
                                 is_active=1, is_superuser=1, is_staff=1, date_joined=timezone.now(), last_name="name")
        em = Employer.objects.create(companyName="company", user=us, description='description')
        response = c.post('/signin/employer', employer=em)
        afterEmp = Employer.objects.get(pk=em.id)

        assert afterEmp.companyName == em.companyName
        assert afterEmp.user.__eq__(em.user)

        assertEquals = (em, afterEmp)


class OfferAddingTest(TestCase):
    def test(self):
        us = User.objects.create(username="testUser", password="test", email="email", last_login=timezone.now(),
                                 is_active=1, is_superuser=1, is_staff=1, date_joined=timezone.now(), last_name="name")
        em = Employer.objects.create(companyName="company", user=us, description='description')

        c = Client()
        of = Offer.objects.create(description="description", startDate=timezone.now(), endDate=timezone.now(),
                                  position="position", branch="branch", company=em)
        response = c.post('offer/new/', offer=of)
        afterOf = Offer.objects.get(pk=of.id)

        assertEquals = (of, afterOf)


class LoginTest(TestCase):
    def test(self):
        us = User.objects.create(username="testUser", password="test", email="email", last_login=timezone.now(),
                                 is_active=1, is_superuser=1, is_staff=1, date_joined=timezone.now(), last_name="name")
        em = Employer.objects.create(companyName="company", user=us, description='description')

        c = Client()
        response = c.post('user/login', {'username': 'testUser', 'password': 'test'})

        assertEquals = (response.status_code, 200)


class SignTest(TestCase):
    def test(self):
        c = Client()
        us = User.objects.create(username="testUser", password="test", email="email", last_login=timezone.now(),
                                 is_active=1, is_superuser=1, is_staff=1, date_joined=timezone.now(), last_name="name")
        response = c.post('/signin/', user=us)
        afterUser = User.objects.get(username="testUser")
        assertEquals = (us, afterUser)


class NoOfferDetailsTest(TestCase):
    def test(self):
        c = Client()
        response=c.get('offer/1700000000')
        self.assertEqual(response.status_code,404)




class CantLoginTest(TestCase):
    def test(self):
        c = Client
        assert (c.login(Client, username='a', password='b') == False)


class Login(TestCase):
    def test(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        assert self.client.login(username='temporary', password='temporary')==True


class ModelTest(TestCase) :
    def test(self):
       us = User.objects.create(username="testUser", password="test", email="email", last_login=timezone.now(),
                                 is_active=1, is_superuser=1, is_staff=1, date_joined=timezone.now(), last_name="name")
       em = Employer.objects.create(companyName="company", user=us, description='description')


       try :
           us2 = User.objects.create(username="testUser", password="test", email="email", last_login=timezone.now(),
                                     is_active=1, is_superuser=1, is_staff=1, date_joined=timezone.now(),
                                     last_name="name")
           em2 = Employer.objects.create(companyName="company", user=us, description='description')
       except IntegrityError :
           assert True
