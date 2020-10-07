from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from ems.models import Department, Employee, User
from ems.serializers import DepartmentSerializer, EmployeeSerializer, UserSerializer

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer