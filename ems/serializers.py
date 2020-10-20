from rest_framework import serializers
from ems.models import Employee, Department, Company
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']        


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'company']


class EmployeeSerializer(serializers.ModelSerializer):
    emp_first_name = serializers.ReadOnlyField(source='user.first_name')
    emp_last_name = serializers.ReadOnlyField(source='user.last_name')
    # dept_name = serializers.ReadOnlyField(source='department.name',many=True)
    # department = DepartmentSerializer(many=True)

    class Meta:
        model = Employee
        fields = ['id', 'user', 'emp_first_name', 'emp_last_name', 'department','designation']
