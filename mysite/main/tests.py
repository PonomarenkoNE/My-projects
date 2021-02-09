from datetime import datetime
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, Post
from .views import home



class SingInTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='1test', password='1test', email='1test@test.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='1test', password='1test')
        self.assertTrue(user is not None)

    def test_wrong_password(self):
        user = authenticate(username='1test', password='wrong')
        self.assertFalse(user is not None)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='1test')
        self.assertFalse(user is not None)


class ViewsTest(TestCase):
    def setUp(self):
        self.data = {
            'username': 'test11',
            'password': 'test'
        }
        self.user = User.objects.create_user(username='test11', password='test', email='test@test.com')
        self.post = Post.objects.create(username='test11', text='testing', date=datetime.now())
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_home(self):
        response = self.client.post(reverse('home'), self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/test11/')

    def test_profile(self):
        self.client.login(username='test11', password='test')
        response = self.client.get(reverse('profile2'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.client.logout()

    def test_posts(self):
        self.client.login(username='test11', password='test')
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')

    def test_feed(self):
        self.client.login(username='test11', password='test')
        response = self.client.get(reverse('myfeed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')

