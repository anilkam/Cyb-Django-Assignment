from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from ems.models import Company, Department, Employee
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

class AdminLoginTest(TestCase):
    def setUp(self):
        (self.username, self.password) = _create_super_user()

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

class CompanyAdminTest(TestCase):
    # Payload obtained from Network -> Headers -> Form Data in Chrome
    company_form_post_payload = {
        "name": "Tester Inc",

        # Department inline in company
        # Need to add these, else get "ManagementForm data is missing or has been tampered with" error
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

    company_form_post_invalid_payload = deepcopy(company_form_post_payload)
    company_form_post_invalid_payload['name'] = ''

    def setUp(self):
        (self.username, self.password) = _create_super_user()

        comp = Company.objects.create(name='Test Company 1')
        self.comp_id = comp.id

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

    def test_company_add_valid_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse('admin:ems_company_add'),
            self.company_form_post_payload,
        )

        company = Company.objects.get(name=self.company_form_post_payload["name"])
        dept = Department.objects.get(company=company)

        self.assertEqual(company.name, self.company_form_post_payload["name"])
        self.assertEqual(dept.name, self.company_form_post_payload["department_set-0-name"])
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_company_add_invalid_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse('admin:ems_company_add'),
            self.company_form_post_invalid_payload,
        )

        self.assertContains(response, 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

        dept = Department.objects.get(company=company)

        self.assertEqual(dept.name, self.company_form_post_payload["department_set-0-name"])
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

class EmployeeAdminTest(TestCase):
    '''
    Test cases for Employee Admin, which also has User inline reverse
    '''
    employee_form_post_payload = {
        # Add department key-value later
        "designation": "As",
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 0,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1,
        "form-0-username": "mikescott",
        "form-0-first_name": "Michael",
        "form-0-last_name": "Scott"
    }

    employee_form_post_invalid_payload = deepcopy(employee_form_post_payload)
    employee_form_post_invalid_payload['designation'] = ''

    def setUp(self):
        (self.username, self.password) = _create_super_user()

        comp = Company.objects.create(name='Test Company 1')
        dept1 = Department.objects.create(name='Engineering', company=comp)

        user1 = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret',
            first_name='Test',
            last_name='User'
        )

        self.emp1 = Employee.objects.create(
            designation='Jr',
            user=user1,
        )

        self.emp1.department.add(dept1)

        self.employee_form_post_payload['department'] = dept1.pk

    def test_load_employee_detail_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.get(
            reverse(
                'admin:ems_employee_change',
                args=(self.emp1.id,),
            )
        )
        emp = Employee.objects.get(id=self.emp1.id)

        self.assertContains(response, emp.user.first_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_add_valid_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse('admin:ems_employee_add'),
            self.employee_form_post_payload,
        )

        user = User.objects.get(username=self.employee_form_post_payload['form-0-username'])
        emp = Employee.objects.get(user=user)

        self.assertEqual(emp.user.first_name, self.employee_form_post_payload["form-0-first_name"])
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_employee_add_invalid_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse('admin:ems_employee_add'),
            self.employee_form_post_invalid_payload,
        )

        self.assertContains(response, 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_change_form(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        # any changes made to a copy of object do not reflect in the original object
        employee_form_post_payload = deepcopy(self.employee_form_post_payload)
        employee_form_post_payload['designation'] = 'As'

        response = self.client.post(
            reverse(
                'admin:ems_employee_change',
                args=(self.emp1.id,),
            ),
            employee_form_post_payload
        )
        employee = Employee.objects.get(id=self.emp1.id)

        self.assertEqual(employee.designation, 'As')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_employee_delete(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            reverse(
                'admin:ems_employee_delete',
                args=(self.emp1.id,),
            ),
            {"post": "yes"}  # Are you sure? button
        )

        deleted = Employee.objects.filter(pk=self.emp1.id).first()
        self.assertEqual(deleted, None)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
