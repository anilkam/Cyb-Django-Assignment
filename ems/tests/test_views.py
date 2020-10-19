from django.test import TestCase
from ems.models import Department, Employee, Company
# from ems.serializers import DepartmentSerializer
# from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


def create_company(name):
    return Company.objects.create(name = name)

class CompanyListViewTest(APITestCase):
    def test_no_companies(self):
        response = self.client.get(reverse('company-list'))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

# 	def test_past_question(self):
# 		create_question(question_text='Past Question.', days=-30)
# 		response = self.client.get(reverse('polls:index'))
# 		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question.>'])

# 	def test_future_question(self):
# 		create_question(question_text='Future Question.', days=30)
# 		response = self.client.get(reverse('polls:index'))
# 		self.assertContains(response, "No polls are available.") 
# 		self.assertQuerysetEqual(response.context['latest_question_list'], [])

# 	def test_future_and_past_question(self):
# 		create_question(question_text='Future Question.', days=30)
# 		create_question(question_text='Past Question.', days=-30)
# 		response = self.client.get(reverse('polls:index'))
# 		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question.>'])

# 	def test_two_past_questions(self):
# 		create_question(question_text='Past Question 1.', days=-30)
# 		create_question(question_text='Past Question 2.', days=-5)
# 		response = self.client.get(reverse('polls:index'))
# 		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question 2.>', '<Question: Past Question 1.>'])

# class QuestionDetailViewTest(TestCase):
# 	def test_future_question(self):
# 		future_question = create_question(question_text='Future Question.', days=5)
# 		url = reverse('polls:detail', args = (future_question.id, ))
# 		response = self.client.get(url)
# 		self.assertEqual(response.status_code, 404)

# 	def test_past_question(self):
# 		past_question = create_question(question_text='Past Question.', days=-5)
# 		url = reverse('polls:detail', args = (past_question.id, ))
# 		response = self.client.get(url)
# 		self.assertContains(response, past_question.question_text)

# class DepartmentModelTest(TestCase):
#     def setUp(self):
#         Department.objects.create(name="HR")

#     def test_dept_created(self):
#         hr = Department.objects.get(id=1)
#         self.assertEqual(hr.name, 'HR')


# class EmployeeModelTest(TestCase):
#     def setUp(self):
#         # get_user_model() to reference our active User
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             email='test@email.com',
#             password='secret'
#             )

#         # self.department = Department.objects.create(name="Engineering")

#         self.employee = Employee.objects.create(
#             designation='Jr',
#             user=self.user,
#             )

#         # Direct assignment to the forward side of a many-to-many set is prohibited, (Can't do department=self.department in create())
#         self.employee.department.create(name="Engineering")

#     def test_emp_created(self):
#         emp = Employee.objects.get(pk=1)
#         self.assertEqual(emp.user.username, 'testuser')

# class DepartmentAPITests(APITestCase):
#     def test_create_dept(self):
#         """
#         Ensure we can create a new department object via API.
#         """
#         url = reverse('department-list')
#         data = {'name': 'Test Dept'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Department.objects.count(), 1)
#         self.assertEqual(Department.objects.get().name, 'Test Dept')

# class GetAllDepartmentsTest(APITestCase):
#     """ Test module for GET all deparments API """

#     def setUp(self):
#         Department.objects.create(name='TD1')
#         Department.objects.create(name='TD2')
#         Department.objects.create(name='TD3')
#         Department.objects.create(name='TD4')

#     def test_get_all_deparments(self):
#         # get API response
#         url = reverse('department-list')
#         response = self.client.get(url)
        
#         from django.test.client import RequestFactory
#         context = {'request': RequestFactory().get(url)}

#         # get data from db
#         depts = Department.objects.all()

#         # When instantiating a HyperlinkedModelSerializer you must include the current request in the serializer context, to ensure that the hyperlinks can include an appropriate hostname, so that the resulting representation uses fully qualified URLs.
#         serializer = DepartmentSerializer(depts, many=True, context=context)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
