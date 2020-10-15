from rest_framework import serializers
from ems.models import Employee, Department, Company
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'first_name', 'last_name']


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'url', 'name']        


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'url', 'name', 'company']


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    emp_first_name = serializers.ReadOnlyField(source='user.first_name')
    emp_last_name = serializers.ReadOnlyField(source='user.last_name')
    # dept_name = serializers.ReadOnlyField(source='department.name',many=True)
    # department = DepartmentSerializer(many=True)

    class Meta:
        model = Employee
        fields = ['id', 'url', 'user', 'emp_first_name', 'emp_last_name', 'department','designation']
