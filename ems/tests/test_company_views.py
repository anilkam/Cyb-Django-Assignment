from ems.models import Company
from ems.serializers import CompanySerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.renderers import JSONRenderer


class GetNoCompaniesTest(APITestCase):
    """ Test module for GET company API when there are no companies"""

    def test_no_companies(self):
        response = self.client.get(reverse('company-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

class GetAllCompaniesTest(APITestCase):
    """ Test module for GET all companies API """

    def setUp(self):
        Company.objects.create(name='Test Company 1')
        Company.objects.create(name='Test Company 2')
        Company.objects.create(name='Test Company 3')
        Company.objects.create(name='Test Company 4')

    def test_get_all_companies(self):
        # get API response
        response = self.client.get(reverse('company-list'))
        # get data from db
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCompanyTest(APITestCase):
    """ Test module for GET single company API """

    def setUp(self):
        # Saving in variable to use self.c1.pk later
        self.c1 = Company.objects.create(name='Test Company 1')
        Company.objects.create(name='Test Company 2')
        Company.objects.create(name='Test Company 3')
        Company.objects.create(name='Test Company 4')

    def test_get_valid_single_company(self):
        response = self.client.get(reverse('company-detail', kwargs={'pk': self.c1.pk}))
        company = Company.objects.get(pk=self.c1.pk)
        serializer = CompanySerializer(company)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_company(self):
        response = self.client.get(reverse('company-detail', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCompanyTest(APITestCase):
    """ Test module for inserting a new company """

    def setUp(self):
        self.valid_payload = {"name":"Tester Inc"}

        self.invalid_payload = {"name":""}

    def test_create_valid_company(self):
        response = self.client.post(
            reverse('company-list'),
            data=JSONRenderer().render(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 1, **self.valid_payload})

    def test_create_invalid_company(self):
        response = self.client.post(
            reverse('company-list'),
            data=JSONRenderer().render(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert error message on name field
        self.assertEqual(response.data, {"name": ["This field may not be blank."]})

class UpdateSingleCompanyTest(APITestCase):
    """ Test module for updating an existing company record """

    def setUp(self):
        self.c1 = Company.objects.create(name='Test Company 1')
        Company.objects.create(name='Test Company 2')
        self.valid_payload = {
            'name': 'Test Tech'
        }

        self.invalid_payload = {
            'name': ''
        }

    def test_valid_update_company(self):
        response = self.client.put(
            reverse('company-detail', kwargs={'pk': self.c1.pk}),
            data=JSONRenderer().render(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': self.c1.pk, **self.valid_payload})

    def test_invalid_update_company(self):
        response = self.client.put(
            reverse('company-detail', kwargs={'pk': 1}),
            data=JSONRenderer().render(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert error message on name field
        self.assertEqual(response.data, {"name": ["This field may not be blank."]})

class DeleteSingleCompanyTest(APITestCase):
    """ Test module for deleting an existing company record """

    def setUp(self):
        self.c1 = Company.objects.create(name='Test Company 1')
        Company.objects.create(name='Test Company 2')
        
    def test_valid_delete_company(self):
        response = self.client.delete(
            reverse('company-detail', kwargs={'pk': self.c1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_company(self):
        response = self.client.delete(
            reverse('company-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
