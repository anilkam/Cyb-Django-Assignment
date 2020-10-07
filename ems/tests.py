from django.test import TestCase
from ems.models import Department, Employee
from django.contrib.auth import get_user_model

class DepartmentModelTest(TestCase):
    def setUp(self):
        Department.objects.create(name="HR")

    def test_dept_created(self):
        hr = Department.objects.get(id=1)
        self.assertEqual(hr.name, 'HR')


class EmployeeModelTest(TestCase):
    def setUp(self):
        # get_user_model() to reference our active User
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
            )

        # self.department = Department.objects.create(name="Engineering")

        self.employee = Employee.objects.create(
            designation='Jr',
            user=self.user,
            )

        # Direct assignment to the forward side of a many-to-many set is prohibited, (Can't do department=self.department in create())
        self.employee.department.create(name="Engineering")

    def test_emp_created(self):
        emp = Employee.objects.get(pk=1)
        self.assertEqual(emp.user.username, 'testuser')
