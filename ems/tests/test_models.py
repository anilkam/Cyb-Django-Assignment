from django.test import TestCase
from ems.models import Company, Department, Employee
from django.contrib.auth import get_user_model


class CompanyModelTest(TestCase):
    # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Company.objects.create(name='Test Industry')

    def test_name_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_company_name(self):
        company = Company.objects.get(id=1)
        expected_object_name = f'{company.name}'
        self.assertEqual(expected_object_name, str(company))


class DepartmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        company = Company.objects.create(name='Test Company')
        Department.objects.create(name='Engineering', company=company)

    def test_name_label(self):
        dept = Department.objects.get(id=1)
        field_label = dept._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        dept = Department.objects.get(id=1)
        max_length = dept._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_company_label(self):
        dept = Department.objects.get(id=1)
        field_label = dept._meta.get_field('company').verbose_name
        self.assertEqual(field_label, 'company')    

    def test_object_name_is_deparment_name_bracket_company_name(self):
        dept = Department.objects.get(id=1)
        expected_object_name = f'{dept.name} ({dept.company.name})'
        self.assertEqual(expected_object_name, str(dept))


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        company = Company.objects.create(name='Test Company')
        
        dept1 = Department.objects.create(name='Engineering', company=company)
        dept2 = Department.objects.create(name='Quality Assurance', company=company)
        
        user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        # self.department = Department.objects.create(name="Engineering")

        employee = Employee.objects.create(
            designation='Jr',
            user=user,
        )

        # Direct assignment to the forward side of a many-to-many set is prohibited, (Can't do department=self.department in create())
        # employee.department.create(name="Engineering")
        employee.department.add(dept1, dept2)

    def test_designation_label(self):
        emp = Employee.objects.get(id=1)
        field_label = emp._meta.get_field('designation').verbose_name
        self.assertEqual(field_label, 'designation')

    def test_designation_max_length(self):
        emp = Employee.objects.get(id=1)
        max_length = emp._meta.get_field('designation').max_length
        self.assertEqual(max_length, 2)

    def test_user_label(self):
        emp = Employee.objects.get(id=1)
        field_label = emp._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')    

    def test_department_label(self):
        emp = Employee.objects.get(id=1)
        field_label = emp._meta.get_field('department').verbose_name
        self.assertEqual(field_label, 'department')    

    def test_object_name_is_user_first_name_space_user_last_name(self):
        emp = Employee.objects.get(id=1)
        expected_object_name = f'{emp.user.first_name} {emp.user.last_name}'
        self.assertEqual(expected_object_name, str(emp))
