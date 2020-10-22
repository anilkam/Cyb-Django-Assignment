from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from ems.models import Company, Department
from copy import deepcopy


def _create_super_user():
    username = 'admin'
    password = User.objects.make_random_password()

    user = User.objects.create_superuser(
        email='admin@admin.com',
        password=password,
        username=username,
    )

    return (username, password)

class AdminTestCase(TestCase):
    # Payload obtained from Network -> Headers -> Form Data in Chrome
    company_form_post_payload = {
        "name": "Tester Inc",

        "department_set-TOTAL_FORMS": 1,
        "department_set-INITIAL_FORMS": 0,
        "department_set-MIN_NUM_FORMS": 0,
        "department_set-MAX_NUM_FORMS": 1000,

        "department_set-0-name": "Quality",

        "department_set-0-Employee_department-TOTAL_FORMS": 3,
        "department_set-0-Employee_department-INITIAL_FORMS": 0,
        "department_set-0-Employee_department-MIN_NUM_FORMS": 0,
        "department_set-0-Employee_department-MAX_NUM_FORMS": 1000
    }

    def setUp(self):
        (self.username, self.password) = _create_super_user()

        comp = Company.objects.create(name='Test Company 1')
        self.comp_id = comp.id

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/login/?next=/admin/')

    def test_response_if_logged_in(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('admin:index'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'admin')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_load_company_detail_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.get(
            reverse(
                'admin:ems_company_change',
                args=(self.comp_id,),
            )
        )
        company = Company.objects.get(id=self.comp_id)

        self.assertContains(response, company.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_add_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse('admin:ems_company_add'),
            self.company_form_post_payload,
        )

        company = Company.objects.get(name=self.company_form_post_payload["name"])
        dept = Department.objects.get(company=company.id)

        self.assertEqual(company.name, self.company_form_post_payload["name"])
        self.assertEqual(dept.name, self.company_form_post_payload["department_set-0-name"])
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


    def test_company_change_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        # any changes made to a copy of object do not reflect in the original object
        company_form_post_payload = deepcopy(self.company_form_post_payload)
        company_form_post_payload['name'] = 'New Company'

        response = self.client.post(
            reverse(
                'admin:ems_company_change',
                args=(self.comp_id,),
            ),
            company_form_post_payload
        )
        company = Company.objects.get(id=self.comp_id)

        self.assertEqual(company.name, 'New Company')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_company_delete(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse(
                'admin:ems_company_delete',
                args=(self.comp_id,),
            ),
            {"post": "yes"}  # Are you sure? button
        )

        deleted = Company.objects.filter(pk=self.comp_id).first()
        self.assertEqual(deleted, None)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
