from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from ems.models import Department, Employee, User, Company
from ems import serializers

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
