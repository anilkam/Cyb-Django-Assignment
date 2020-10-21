from ems.models import Company, Department
from ems.serializers import DepartmentSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.renderers import JSONRenderer


class GetNoDepartmentsTest(APITestCase):
    """ Test module for GET department API when there are no departments"""

    def test_no_deparments(self):
        response = self.client.get(reverse('department-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

class GetAllDepartmentsTest(APITestCase):
    """ Test module for GET all departments API """

    def setUp(self):
        c1 = Company.objects.create(name='Test Company 1')
        c2 = Company.objects.create(name='Test Company 2')

        Department.objects.create(name='Test Dept 1', company=c1)
        Department.objects.create(name='Test Dept 2', company=c1)
        Department.objects.create(name='Test Dept 3', company=c2)
        Department.objects.create(name='Test Dept 4', company=c2)

    def test_get_all_departments(self):
        # get API response
        response = self.client.get(reverse('department-list'))
        # get data from db
        depts = Department.objects.all()
        serializer = DepartmentSerializer(depts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleDepartmentTest(APITestCase):
    """ Test module for GET single department API """

    def setUp(self):
        c1 = Company.objects.create(name='Test Company 1')
        c2 = Company.objects.create(name='Test Company 2')

        self.test_dept = Department.objects.create(name='Test Dept 1', company=c1)
        Department.objects.create(name='Test Dept 2', company=c1)
        Department.objects.create(name='Test Dept 3', company=c2)
        Department.objects.create(name='Test Dept 4', company=c2)

    def test_get_valid_single_department(self):
        response = self.client.get(reverse('department-detail', kwargs={'pk': self.test_dept.pk}))
        department = Department.objects.get(pk=self.test_dept.pk)
        serializer = DepartmentSerializer(department)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_department(self):
        response = self.client.get(reverse('department-detail', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewDepartmentTest(APITestCase):
    """ Test module for inserting a new department """

    def setUp(self):
        c1 = Company.objects.create(name='Test Company 1')

        self.valid_payload = {"name":"Tester Inc", "company": c1.pk}

        self.invalid_payload = {"name":""}

    def test_create_valid_department(self):
        response = self.client.post(
            reverse('department-list'),
            data=JSONRenderer().render(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 1, **self.valid_payload})

    def test_create_invalid_department(self):
        response = self.client.post(
            reverse('department-list'),
            data=JSONRenderer().render(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert error message on name field
        self.assertEqual(response.data, {
            "name": ["This field may not be blank."],
            "company": ["This field is required."]
            })

class UpdateSingleDepartmentTest(APITestCase):
    """ Test module for updating an existing department record """

    def setUp(self):
        c1 = Company.objects.create(name='Test Company 1')
        self.test_dept = Department.objects.create(name='Test Dept 1', company=c1)
        Department.objects.create(name='Test Dept 2', company=c1)

        self.valid_payload = {"name":"Tester Inc", "company": c1.pk}

        self.invalid_payload = {"name":""}
        
    def test_valid_update_department(self):
        response = self.client.put(
            reverse('department-detail', kwargs={'pk': self.test_dept.pk}),
            data=JSONRenderer().render(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': self.test_dept.pk, **self.valid_payload})

    def test_invalid_update_department(self):
        response = self.client.put(
            reverse('department-detail', kwargs={'pk': self.test_dept.pk}),
            data=JSONRenderer().render(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert error messages
        self.assertEqual(response.data, {
            "name": ["This field may not be blank."],
            "company": ["This field is required."]
            })

class DeleteSingleDepartmentTest(APITestCase):
    """ Test module for deleting an existing department record """

    def setUp(self):        
        c1 = Company.objects.create(name='Test Company 1')
        self.test_dept = Department.objects.create(name='Test Dept 1', company=c1)
        Department.objects.create(name='Test Dept 2', company=c1)

    def test_valid_delete_department(self):
        response = self.client.delete(
            reverse('department-detail', kwargs={'pk': self.test_dept.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        deleted = Department.objects.filter(pk=self.test_dept.pk).first()
        self.assertEqual(deleted, None)

    def test_invalid_delete_department(self):
        response = self.client.delete(
            reverse('department-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
