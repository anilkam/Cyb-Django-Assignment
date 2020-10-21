from ems.models import Company, Department, Employee
from ems.serializers import EmployeeSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User


class GetNoEmployeesTest(APITestCase):
    """ Test module for GET company API when there are no employees"""

    def test_no_employees(self):
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

class GetAllEmployeesTest(APITestCase):
    """ Test module for GET all employees API """

    def setUp(self):
        c1 = Company.objects.create(name='Test Company 1')

        dept1 = Department.objects.create(name='Engineering', company=c1)
        dept2 = Department.objects.create(name='Quality Assurance', company=c1)
        dept3 = Department.objects.create(name='Human Resources', company=c1)
        
        user1 = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        emp1 = Employee.objects.create(
            designation='Jr',
            user=user1,
        )

        emp1.department.add(dept1, dept2)

        user2 = User.objects.create_user(
            username='user2',
            email='test2@email.com',
            password='secret'
        )

        emp2 = Employee.objects.create(
            designation='Sr',
            user=user2,
        )

        emp2.department.add(dept3)

    def test_get_all_employees(self):
        # get API response
        response = self.client.get(reverse('employee-list'))
        # get data from db
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleEmployeeTest(APITestCase):
    """ Test module for GET single employee API """

    def setUp(self):
        c1 = Company.objects.create(name='Test Company 1')

        dept1 = Department.objects.create(name='Engineering', company=c1)
        dept2 = Department.objects.create(name='Quality Assurance', company=c1)
        dept3 = Department.objects.create(name='Human Resources', company=c1)
        
        user1 = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.emp1 = Employee.objects.create(
            designation='Jr',
            user=user1,
        )

        self.emp1.department.add(dept1, dept2)

        user2 = User.objects.create_user(
            username='user2',
            email='test2@email.com',
            password='secret'
        )

        emp2 = Employee.objects.create(
            designation='Sr',
            user=user2,
        )

        emp2.department.add(dept3)

    def test_get_valid_single_employee(self):
        response = self.client.get(reverse('employee-detail', kwargs={'pk': self.emp1.pk}))
        employee = Employee.objects.get(pk=self.emp1.pk)
        serializer = EmployeeSerializer(employee)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_employee(self):
        response = self.client.get(reverse('employee-detail', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

'''
class CreateNewEmployeeTest(APITestCase):
    """ Test module for inserting a new company """

    def setUp(self):
        self.valid_payload = {"name":"Tester Inc"}

        self.invalid_payload = {"name":""}

    def test_create_valid_employee(self):
        response = self.client.post(
            reverse('employee-list'),
            data=JSONRenderer().render(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 1, **self.valid_payload})

    def test_create_invalid_employee(self):
        response = self.client.post(
            reverse('employee-list'),
            data=JSONRenderer().render(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert error message on name field
        self.assertEqual(response.data, {"name": ["This field may not be blank."]})

class UpdateSingleEmployeeTest(APITestCase):
    """ Test module for updating an existing employee record """

    def setUp(self):
        self.c1 = Company.objects.create(name='Test Company 1')
        Company.objects.create(name='Test Company 2')
        self.valid_payload = {
            'name': 'Test Tech'
        }

        self.invalid_payload = {
            'name': ''
        }

    def test_valid_update_employee(self):
        response = self.client.put(
            reverse('employee-detail', kwargs={'pk': self.c1.pk}),
            data=JSONRenderer().render(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': self.c1.pk, **self.valid_payload})

    def test_invalid_update_employee(self):
        response = self.client.put(
            reverse('employee-detail', kwargs={'pk': 1}),
            data=JSONRenderer().render(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert error message on name field
        self.assertEqual(response.data, {"name": ["This field may not be blank."]})

class DeleteSingleEmployeeTest(APITestCase):
    """ Test module for deleting an existing employee record """

    def setUp(self):
        self.c1 = Company.objects.create(name='Test Company 1')
        Company.objects.create(name='Test Company 2')
        
    def test_valid_delete_employee(self):
        response = self.client.delete(
            reverse('employee-detail', kwargs={'pk': self.c1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_employee(self):
        response = self.client.delete(
            reverse('employee-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
'''