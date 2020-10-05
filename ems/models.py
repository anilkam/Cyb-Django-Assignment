from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

class Employee(models.Model):
    DESIGNATIONS = [
        ('Jr', 'Junior'),
        ('As', 'Associate'),
        ('Sr', 'Senior'),
        ('Mg', 'Manager'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(choices=DESIGNATIONS, max_length=2)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"