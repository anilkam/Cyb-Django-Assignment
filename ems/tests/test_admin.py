from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AdminTestCase(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_superuser(username='testuser1', password='1X<ISRUkw+tuK')
        
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
            response = self.client.get(reverse('admin:index'))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, '/admin/login/?next=/admin/')

    def test_response_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('admin:index'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_response_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/admin/ems/employee/')
        # print(response.)
        # Check our user is logged in
        # self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
